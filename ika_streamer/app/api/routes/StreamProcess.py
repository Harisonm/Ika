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
    
    first_topic = 'gmail_message_id'
    Second_topic = 'gmail_corps'
    acks='all'
    
    try:
        # Remplacer le name de new topcis par adresse email ou ID unique
        # Création du premier Topic -> Message_id
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic = NewTopic(name=first_topic,num_partitions=4,replication_factor=2)
        admin.create_topics(first_topic)
        
        # Création du deuxième Topic -> Gmail_corp
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic = NewTopic(name=Second_topic,num_partitions=4,replication_factor=2)
        admin.create_topics(Second_topic)
        
    except Exception:
        pass
    
    try:
        IkaProducer(topic_name=first_topic, data=message_id,acks=acks).run()
    except Exception:
        pass
    
    consumer = KafkaConsumer(
        first_topic,                                # specify topic to consume from
        bootstrap_servers=bootstrap_servers,
        # consumer_timeout_ms=3000,                       # break connection if the consumer has fetched anything for 3 secs (e.g. in case of an empty topic)
        auto_offset_reset='earliest',                   # automatically reset the offset to the earliest offset (should the current offset be deleted or anything)
        enable_auto_commit=False,                        # offsets are committed automatically by the consumer
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Consumer constructed')
        
    try:
        while True:
            logging.info("About to call consumer.poll for new messages")
            # messages = consumer.poll()
            logging.info("Finished consumer.poll, now process_messages")
            for message in consumer:                            # loop over messages
                logging.info('Offset: %s', message.offset)
                messages_id = message.value
                print(messages_id)
                
                mail_df = pd.DataFrame.from_records(GmailCollecterModel("prod",transform_flag=transform_flag).collect_mail(user_id="me",
                                                                                                    message_id=messages_id,
                                                                                                    max_workers=max_workers),columns=["idMail","threadId","historyId","from","to","date","labelIds","spam","body","mimeType"]).to_json(orient="index")
                print(mail_df)
                return JSONResponse(content=mail_df)
            logging.info("Finished process_messages, now committing new offsets")
            consumer.commit()
        
        consumer.close()
    
    except Exception:
        pass
        
  
    # try:
        
    #     IkaProducer(topic_name=Second_topic, data=mail_df,acks=acks).run()
        
    # except Exception as e:
    #     logging.error('Error: %s',e)
