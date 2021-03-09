import json
from typing import Dict, Tuple

from google.cloud import pubsub_v1, secretmanager
from google.cloud.pubsub_v1.subscriber.message import Message
from concurrent.futures import TimeoutError
import os
import requests
from background_task import background
from graphql_jwt.shortcuts import get_refresh_token
from configs.configs import GCP_KEYFILE_PATH

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_KEYFILE_PATH

PROJECT_ID = 'mirrormedia-1470651750304'
timeout = 60

# Secret
secret_client = secretmanager.SecretManagerServiceClient()


def read_secret(secret_name: str, version: str) -> Dict:
    """Read and decode secret from GCP secret"""
    # secret_name = data[
    #     'secret_name']  # 'mm-gateway-token' "saleor-mirror-token-for-mm-apigateway-dev"
    # version = data["version"]
    response = secret_client.access_secret_version(
        name=f"projects/983956931553/secrets/{secret_name}/versions/{version}")

    payload = response.payload.data.decode("UTF-8")

    secret = json.loads(payload)
    return secret


def update_secret(secret_name: str, old_version: str) -> Tuple:
    """Update secret from refresh_token in old_secret and return complete message"""

    # secret_name = data[
    #     'secret_name']
    # 'mm-gateway-token' "saleor-mirror-token-for-mm-apigateway-dev"
    # version = data['version']

    secret_client.disable_secret_version(
        name=f"projects/983956931553/secrets/{secret_name}/versions/{old_version}")

    old_secret = read_secret(secret_name, old_version)
    refresh_token = get_refresh_token(old_secret['refresh_token'])
    new_secret = get_renew_token(refresh_token)
    refresh_token.revoke()

    response = secret_client.add_secret_version(
        parent=secret_name, payload={"data": json.dumps(new_secret).encode('utf-8')}
    )
    # complete_message = {"secret_name": secret_name,
    #           "version": response.name.split('/')[-1]}
    old_version = response.name.split('/')[-1]
    return secret_name, old_version


def get_renew_token(refresh_token: str) -> Dict:
    # TODO:Try another better way to do this.
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


def receive_refresh_request(message: Message):
    """Refresh the token when received message"""
    # print(f"Received {message}.", type(message))
    secret_name = message.attributes.secret_name
    old_version = message.attributes.version  # String
    message.ack()

    # secret = read_secret(secret_name, old_version)
    secret_name, version = update_secret(secret_name, old_version)

    publish_complete_message(secret_name, version)


def publish_complete_message(secret_name: str, version: str):
    """Publish complete message to Pub/Sub"""
    publish_topic = 'update_token'
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, publish_topic)

    # data = json.dumps(complete_message).encode('utf-8')
    future = publisher.publish(topic_path, data=b'', secret_name=secret_name,
                               version=version)


@background(schedule=timeout)
def listening():
    subscription_topic = 'renew_token'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, subscription_topic)

    streaming_pull_future = subscriber.subscribe(subscription_path,
                                                 callback=receive_refresh_request)
    print(f"Listening for messages on {subscription_path}..\n")
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
