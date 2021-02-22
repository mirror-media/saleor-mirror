from apps.user.models import CustomUser
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
from configs.configs import ENV
import os

# https://googleapis.dev/python/pubsub/latest/index.html

# os.environ[
#     'GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
#     os.path.split(os.path.abspath(__file__))[0],
#     'configs/saleor_keyfile.json')
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/andy/mirror/saleor-mirror/configs/saleor_keyfile.json'

PROJECT_ID = 'mirrormedia-1470651750304'
timeout = 60


def cron_simple():
    print("SIMPLE TEST")


def get_message(message: Message):
    firebase_id = message.attributes.get('firebaseID')
    action = message.attributes.get('action', 'delete')  # String
    message.ack()

    if action == 'delete':
        CustomUser.objects.get(firebase_id=firebase_id).delete()
        print(f"Member with firebase id {firebase_id} is deleted ")
        return "Done"
    else:
        return "Error"

def publish_delete_request():
    firebase_id = 'test0222'
    action = 'delete'
    publish_topic = f'mm-member-saleor.{ENV}'
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, publish_topic)
    future = publisher.publish(topic_path, data=b'', firebaseID=firebase_id,
                               action=action)


def delete_member():
    subscriber = pubsub_v1.SubscriberClient()
    topic_name = f"projects/mirrormedia-1470651750304/topics/mm-member.{ENV}"
    subscription_name = f"projects/mirrormedia-1470651750304/subscriptions/mm-member-saleor.{ENV}"

    streaming_pull_future = subscriber.subscribe(subscription_name,
                                                 callback=get_message)

    print(f"Listening for messages on {subscription_name}..\n")
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
