#!/usr/bin/env python
import threading, time

from kafka import KafkaConsumer, KafkaProducer
import os

KAFKA_URI_1=os.environ.get("KAFKA_URI_1", default=False)
KAFKA_URI_2=os.environ.get("KAFKA_URI_2", default=False)
KAFKA_URI_3=os.environ.get("KAFKA_URI_3", default=False)
bootstrap_servers = [KAFKA_URI_1,KAFKA_URI_2,KAFKA_URI_3]

class IkaConsumer(threading.Thread):
    def __init__(self,topic_name):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic_name = topic_name

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe([self.topic_name])

        while not self.stop_event.is_set():
            for message in consumer:
                if self.stop_event.is_set():
                    break

        consumer.close()