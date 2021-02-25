import logging

from django.core.management import BaseCommand

from apps.user.models import CustomUser
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from apps.user.schema import md5, delete_update
from configs.configs import ENV
import os
from configs.configs import GCP_KEYFILE_PATH

# https://googleapis.dev/python/pubsub/latest/index.html

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_KEYFILE_PATH

PROJECT_ID = 'mirrormedia-1470651750304'
timeout = 60


def process_deletion(message: Message):
    firebase_id = message.attributes.get('firebaseID')
    action = message.attributes.get('action', 'delete')  # String
    # message.ack()

    if action == 'delete':
        try:
            member_instance = CustomUser.objects.get(firebase_id=firebase_id)
            if member_instance and member_instance.is_active == True:
                delete_update(member_instance)

            print(f"Member with firebase id {firebase_id} is deleted")
            message.ack()
            return firebase_id
        except CustomUser.DoesNotExist:
            print(f"Member with firebase id {firebase_id} does not exist")
    else:
        message.nack()
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
                                                 callback=process_deletion)

    print(f"Listening for messages on {subscription_name}..\n")
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()


class Command(BaseCommand):
    help = "Subscribe to GCP Pub/Sub to delete member"

    def handle(self, *args, **options):
        try:
            delete_member()
            # self.stdout.write(self.style.SUCCESS(f"Successfully deleted member with firebase_id {firebase_id}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"FAILED for {e.args[0]}"))
