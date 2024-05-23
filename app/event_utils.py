import pika
import json
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange='user_events', exchange_type='topic', durable=False)
    return channel

def publish_event(event_type, data):
    channel = setup_rabbitmq()
    event = {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'serviceOrigin': 'NameService',
        'traceId': str(uuid.uuid4()),
        'eventType': event_type,
        'environment': 'production',
        'payload': data
    }
    channel.basic_publish(
        exchange='user_events', 
        routing_key=f'userManagement.{event_type}', 
        body=json.dumps(event))
    logging.info(f"Event published: {event_type} with data: {data}")
    channel.close()
