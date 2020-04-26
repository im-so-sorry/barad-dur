import json
import logging
from collections import defaultdict
from time import sleep
from typing import List, Callable, Any, Dict

from django.conf import settings
from django.core.management import BaseCommand
from googleapiclient.channel import Notification
from kafka import KafkaConsumer, KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord

from apps.social.models import NotificationService
from apps.stream.models import Event
from apps.user.models import SocialUser, User

system_logger = logging.getLogger("system")


class Command(BaseCommand):
    help = 'Handling events from kafka'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.bootstrap_servers = settings.KAFKA_HOSTS
        self.group_id = settings.KAFKA_GROUP_ID
        self.topics = settings.KAFKA_STREAM_TOPICS
        self.auto_offset_reset = settings.KAFKA_AUTO_OFFSET_RESET or 'earliest'
        self.session_timeout_ms = 6000
        self.enable_auto_commit = settings.KAFKA_ENABLE_AUTO_COMMIT or True

        self.produce_topic_basename = "notification"

        self.consumer = None
        self.producer = None

    def get_producer(self) -> KafkaProducer:
        if self.producer is None:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
        return self.producer

    def get_consumer(self, topics: List[str] = None) -> KafkaConsumer:

        if not topics:
            topics = self.topics

        if self.consumer is None:
            self.consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset=self.auto_offset_reset,
                session_timeout_ms=self.session_timeout_ms,
                enable_auto_commit=self.enable_auto_commit,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )

        return self.consumer

    def handle(self, *args, **options):
        self.listen()

    def listen(self, message_handler: Callable[[ConsumerRecord], Any] = None, rise_exception=False):
        """
        Start topic listening
        :param message_handler:
        :return:
        """
        system_logger.info(f'Start listen')
        system_logger.info(f'Get consumer')

        consumer = self.get_consumer()

        if message_handler is None:
            message_handler = self.process_message

        system_logger.info(f'Start msg in consumer')
        for msg in consumer:
            try:
                result = message_handler(msg)

            except Exception as e:
                if rise_exception:
                    raise e
                else:
                    logging.error(str(e))

    def create_event(self, msg: ConsumerRecord, force_save: bool = True):
        service = msg.topic.split("_", maxsplit=1)[0]

        event_body = msg.value.get("event")

        event = Event(
            service=service or "vk",
            event_type=event_body.get('event_type'),
            tags=event_body.get('tags', []),
            payload=event_body
        )

        if force_save:
            event.save()

        return event

    def get_users(self, tags: List[str]):
        return User.objects.filter(rules__key__in=tags).all()

    def get_notifications(self, users):
        qs = NotificationService.objects.filter(
            user__in=users, is_active=True,
        ).order_by("service")
        return qs

    def send_notifications(self, service: str, notifications: List[NotificationService], event: Dict):
        producer = self.get_producer()

        topic = "{}_{}".format(service, self.produce_topic_basename)

        data = {
            "user_ids": [notification.value for notification in notifications],
            "event": event
        }
        return producer.send(topic, data)

    def process_message(self, msg: ConsumerRecord) -> Any:
        message: Dict = msg.value

        instance = self.create_event(msg)

        users = self.get_users(instance.tags)
        notifications = self.get_notifications(users)

        service_notifications = defaultdict(list)

        for notification in notifications:
            service_notifications[notification.service].append(notification)

        for service, notifications in service_notifications.items():
            self.send_notifications(service, notifications, message.get("event"))
