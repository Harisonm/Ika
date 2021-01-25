#!/usr/bin/env python
import threading, time

from kafka import KafkaConsumer, KafkaProducer
import os,json

KAFKA_URI_1=os.environ.get("KAFKA_URI_1", default=False)
KAFKA_URI_2=os.environ.get("KAFKA_URI_2", default=False)
KAFKA_URI_3=os.environ.get("KAFKA_URI_3", default=False)
bootstrap_servers = [KAFKA_URI_1,KAFKA_URI_2,KAFKA_URI_3]

class ProducerGmail(threading.Thread):
    def __init__(self,topic_name,data):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic_name = topic_name
        self.data = data

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        while not self.stop_event.is_set():
            producer.send(self.topic_name, self.data)
            time.sleep(1)

        producer.close()
