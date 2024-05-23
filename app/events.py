import logging
from .crud import create_name, delete_name
from .database import SessionLocal
from .schemas import NameCreate
import json
from .event_utils import setup_rabbitmq

logging.basicConfig(level=logging.INFO)

def start_listeners():
    channel = setup_rabbitmq()
    queue_result = channel.queue_declare('', exclusive=True)
    queue_name = queue_result.method.queue

    channel.queue_bind(exchange='user_events', queue=queue_name, routing_key='userManagement.userCreated')
    channel.queue_bind(exchange='user_events', queue=queue_name, routing_key='userManagement.userDeleted')

    def callback(ch, method, properties, body):
        logging.info(f"Received message: {body}")
        with SessionLocal() as db:
            if method.routing_key == 'userManagement.userCreated':
                data = json.loads(body)
                create_name(db, NameCreate(id=data['payload']['id'], name=None))
            elif method.routing_key == 'userManagement.userDeleted':
                data = json.loads(body)
                delete_name(db, data['payload']['id'])

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    logging.info("Starting to consume")
    channel.start_consuming()

if __name__ == "__main__":
    start_listeners()
