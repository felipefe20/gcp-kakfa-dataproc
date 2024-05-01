import time
import random
import numpy as np
import threading
from confluent_kafka import SerializingProducer, Producer
from configparser import ConfigParser
import json
import logging
from datetime import datetime
from statsbombpy import sb
from config import config
import socket

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


# Configuration de Kafka

kafka_config = config["kafka"] | {
        'client.id': socket.gethostname()
    }

producer = Producer(kafka_config)

import simplejson
import time
from datetime import datetime

def send_to_kafka(topic, data):
    # Sort data by timestamp
    data = data.sort_values('timestamp')

    # Get the first timestamp
    first_timestamp = data.iloc[0]['timestamp']
    first_timestamp = datetime.strptime(first_timestamp, '%H:%M:%S.%f')  # adjust the format as per your timestamp

    for index, row in data.iterrows():
        # Calculate delay
        print(row['timestamp'], first_timestamp)
        current_timestamp = datetime.strptime(row['timestamp'], '%H:%M:%S.%f')  # adjust the format as per your timestamp
        delay = (current_timestamp - first_timestamp).total_seconds()

        # Delay sending the message
        time.sleep(delay)

        try:
            
            serialized_data = simplejson.dumps(row.to_dict(), ignore_nan=True).replace("\n","").encode('utf-8')
            producer.produce(topic=topic, value=serialized_data)
        except Exception as e:
            logging.error(f"Error serializing data for Kafka: {e}")

        # Update first_timestamp
        first_timestamp = current_timestamp

    producer.flush()

if __name__ == "__main__":
    # Replace 'my-topic' with your topic
    events=sb.events(match_id=3890561)
    my_topic='gcp-confluent-topic-1'
    send_to_kafka(my_topic, events[:100])

