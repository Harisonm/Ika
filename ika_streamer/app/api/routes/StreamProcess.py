from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from ikamail.GmailHelper import GmailHelper
from app.api.models.Gmail.GmailCollecterModel import GmailCollecterModel
from app.api.models.Consumer.IkaConsumer import IkaConsumer
from app.api.models.Producer.IkaProducer import IkaProducer
from app.api.models.Gmail.GmailSchema import GmailOut
from app.api.models.Consumer.ConsumerGmail import ConsumerGmail
from app.api.models.Producer.ProducerGmail import ProducerGmail
from kafka import KafkaConsumer, TopicPartition
from bson.json_util import dumps
from typing import List
from pandas.io.json import json_normalize
from pandas import DataFrame
from kafka.admin import NewTopic
from kafka import KafkaAdminClient

import pandas as pd
import json, time
import logging
import os 
from fastapi.responses import HTMLResponse,JSONResponse
from json import loads

import threading, time
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

KAFKA_URI_1=os.environ.get("KAFKA_URI_1", default=False)
KAFKA_URI_2=os.environ.get("KAFKA_URI_2", default=False)
KAFKA_URI_3=os.environ.get("KAFKA_URI_3", default=False)
bootstrap_servers = [KAFKA_URI_1,KAFKA_URI_2,KAFKA_URI_3]

StreamProcess = APIRouter()

@StreamProcess.get('/BuildMail')
async def BuildMail(next_token: bool=True, transform_flag: bool=True, include_spam_trash: bool=False, max_results:int=200, max_workers:int=100, file_return:str=None):
    """
    create_stream: 

    Args:
    
        next_token (bool, optional): if Flag True -> Take nextPageToken else False -> Take by batch. Defaults to True.
        transform_flag (bool, optional): Using this flag if you want used Transformer Model. Defaults to True.
        include_spam_trash (bool, optional): Include messages from SPAM and TRASH in the results.. Defaults to False.
        max_results (int, optional): Maximum number of messages to return.. Defaults to 25.
        max_workers (int, optional): Maximun number of worker used by multithreading. Defaults to 25.
        file_return (str, optional): Type of file returned by API. Defaults to None.

    Raises:
    
        HTTPException: [description]

    Returns:
    
        API, Json, Csv: Return streaming data from Ika's streamer
    """
    message_id = GmailHelper("prod").get_message_id(
        "me",
        include_spam_trash=include_spam_trash,
        max_results=max_results,
        batch_using=next_token
    )
    
    topic_name = 'mirana-mail-id'
    new_topics_name = 'mirana-mail-decode'
    
    try:
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        
        # Remplacer le name de new topcis par adresse email ou ID unique
        topic = NewTopic(name=topic_name,num_partitions=4,replication_factor=2)
        admin.create_topics(topic_name)
        
    except Exception:
        pass
    

    IkaProducer(topic_name, message_id).run()
    
    consumer = KafkaConsumer(
        topic_name,                                # specify topic to consume from
        bootstrap_servers=bootstrap_servers,
        consumer_timeout_ms=3000,                       # break connection if the consumer has fetched anything for 3 secs (e.g. in case of an empty topic)
        auto_offset_reset='earliest',                   # automatically reset the offset to the earliest offset (should the current offset be deleted or anything)
        enable_auto_commit=False,                        # offsets are committed automatically by the consumer
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Consumer constructed')
        
    try:
        for message in consumer:                            # loop over messages
            logging.info('Offset: %s', message.offset)
            messages_id = message.value
        
        consumer.close()
        
        mail_df = pd.DataFrame.from_records(GmailCollecterModel("prod",
                                                           transform_flag=transform_flag).collect_mail(user_id="me",
                                                                                                       message_id=messages_id,
                                                                                                       max_workers=max_workers), columns=["idMail","threadId","historyId","from","to","date","labelIds","spam","body","mimeType"]).to_json(orient="index")        
        topic = NewTopic(name=new_topics_name,
                        num_partitions=4,
                        replication_factor=2)
        admin.create_topics(new_topics_name)
        
        tasks = [
            ProducerGmail(new_topics_name,mail_df),
            ConsumerGmail(new_topics_name)
        ]

        # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
        for t in tasks:
            t.start()

        time.sleep(10)

        # Stop threads
        for task in tasks:
            task.stop()

        for task in tasks:
            task.join()
        
    except Exception as e:
        logging.error('Error: %s',e)
        
