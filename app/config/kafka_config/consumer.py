import json
import os
from types import FunctionType
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv(verbose=True)


def create_kafka_consumer(topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='terror_events_group',
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )


def consume(topic: str, function: FunctionType, mode: str = 'latest', group: str = None):
    consumer_args = {
        "bootstrap_servers": os.environ['BOOTSTRAP_SERVERS'].replace(" ", "").split(','),
        "value_deserializer": lambda v: json.loads(v.decode('utf-8')),
        "auto_offset_reset": mode,
        "enable_auto_commit": True,
    }
    if group:
        consumer_args["group_id"] = group

    consumer = KafkaConsumer(topic, **consumer_args)

    for message in consumer:
        function(message.value)
