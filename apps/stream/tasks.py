import json

from kafka import KafkaProducer

from app import settings
from apps.core.celery import app


class KafkaClient:

    def __init__(self, *args, **kwargs):
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


kafka_client = KafkaClient()


@app.task
def sync_vk_rules():
    print("test")


@app.task
def add_rule(tag, value):
    producer = kafka_client.get_producer()
    producer.send(
        settings.KAFKA_COMMAND_TOPIC,
        value={
            "content": {
                "command_type": "add",
                "rule": {
                    "tag": tag,
                    "value": value
                }
            },
            "meta": {
                "command_type": "add",
                "tag": tag,
                "value": value
            }
        }
    )


@app.task
def remove_rule(tag):
    producer = kafka_client.get_producer()
    producer.send(
        settings.KAFKA_COMMAND_TOPIC,
        value={
            "content": {
                "command_type": "remove",
                "rule": {
                    "tag": tag,
                }
            },
            "meta": {
                "command_type": "remove",
                "tag": tag,
            }
        }
    )


@app.task
def list_rules():
    producer = kafka_client.get_producer()
    producer.send(
        settings.KAFKA_COMMAND_TOPIC,
        value={
            "content": {
                "command_type": "list",
                "rule": {}
            },
            "meta": {
                "command_type": "list",
            }
        }
    )
