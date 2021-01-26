#!/usr/bin/env python
import threading, time
from kafka import KafkaConsumer, KafkaProducer
import os,json
import logging

KAFKA_URI_1=os.environ.get("KAFKA_URI_1", default=False)
KAFKA_URI_2=os.environ.get("KAFKA_URI_2", default=False)
KAFKA_URI_3=os.environ.get("KAFKA_URI_3", default=False)
bootstrap_servers = [KAFKA_URI_1,KAFKA_URI_2,KAFKA_URI_3]

class IkaProducer():
    def __init__(self,**kwargs):
        self.topic_name = kwargs.get('topic_name', None)
        self.data = kwargs.get('data', None)
        self.acks = kwargs.get('acks', None)

    def run(self):
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                 acks=self.acks,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        # produce asynchronously with callbacks
        producer.send(self.topic_name, self.data).add_callback(self.on_send_success).add_errback(self.on_send_error)
        time.sleep(1)

        # block until all async messages are sent
        producer.flush()
    
    @staticmethod
    def on_send_success(record_metadata):
        logging('topic: %s',record_metadata.topic)
        logging('partition: %s',record_metadata.partition)
        logging('offset: %s',record_metadata.offset)
    
    @staticmethod
    def on_send_error(excp):
        logging.error('I am an errback', exc_info=excp)
    # handle exception