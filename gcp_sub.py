import json
from google.cloud import pubsub_v1, secretmanager
from concurrent.futures import TimeoutError
import os
import requests
from background_task import background
from graphql_jwt.shortcuts import get_refresh_token

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.path.split(os.path.abspath(__file__))[0],
    'configs/saleor_keyfile.json')
# '/Users/andy/mirror/saleor-mirror/configs/saleor_keyfile.json'

PROJECT_ID = 'mirrormedia-1470651750304'
TOPIC_NAME = 'gateway-saleor'
SUB = 'renew_token'
timeout = 60

# Pub/Sub
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUB)

# Secret
secret_client = secretmanager.SecretManagerServiceClient()


def read_secret(payload):
    data = json.loads(payload)
    if data["type"] == 'request':
        secret_name = data['secret_name']  # 'mm-gateway-token'
        version = data["version"]
        response = secret_client.access_secret_version(
            name=f"projects/983956931553/secrets/{secret_name}/versions/{version}")
        payload = response.payload.data.decode("UTF-8")
        secret = json.loads(payload)
        return secret


def update_secret(payload):
    if not isinstance(payload, dict):
        data = json.loads(payload)
    else:
        data = payload

    secret_name = data['secret_name']  # 'mm-gateway-token'
    version = data['version']

    secret_client.disable_secret_version(name=f"{secret_name}/versions/{version}")

    old_secret = read_secret(payload)
    refresh_token = get_refresh_token(old_secret['refresh_token'])
    new_secret = get_renew_token(refresh_token)
    refresh_token.revoke()

    response = secret_client.add_secret_version(
        parent=secret_name, payload={"data": json.dumps(new_secret).encode('utf-8')}
    )
    return {"type": "complete", "secret_name": secret_name,
            "version": response.name.split('/')[-1]}


def get_renew_token(refresh_token):
    gql = f"""
    mutation{{refreshToken(refreshToken:"{refresh_token}"){{
        token
        refreshToken
        success
      }}
    }}
    """
    token = requests.post("http://saleor-mirror.default.svc.cluster.local/graphql/",
                          json={"query": gql})
    token = token.json()

    return token['data']['refreshToken']


def callback(message):
    """Revoke the token when received message"""
    print(f"Received {message}.", type(message))
    message.ack()

    secret = read_secret(message.data.decode('utf-8'))
    complete_message = update_secret(secret)

    publish_secret(complete_message)


def publish_secret(complete_message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, 'gateway-saleor')

    data = json.dumps(complete_message).encode('utf-8')
    future = publisher.publish(topic_path, data=data)


@background(schedule=timeout)
def listening():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
