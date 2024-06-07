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
    logging.info(f"Publishing event: {event_type} with data: {data}")
    try:
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.exchange_declare(exchange='user_events', exchange_type='topic', durable=False)
        event = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'serviceOrigin': 'NameService',
            'traceId': str(uuid.uuid4()),
            'eventType': event_type,
            'environment': 'development',
            'payload': data
        }
        channel.basic_publish(
            exchange='user_events', 
            routing_key=f'userManagement.{event_type}', 
            body=json.dumps(event))
        logging.info(f"Successfully published event: {event_type} with data: {data}")
        connection.close()
    except Exception as e:
        logging.error(f"Failed to publish event: {event_type} with error: {str(e)}")

