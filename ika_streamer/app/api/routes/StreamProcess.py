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
from loguru import logger
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
async def BuildMail(next_token: bool=False, transform_flag: bool=True, include_spam_trash: bool=False, max_results:int=200, max_workers:int=100, file_return:str=None):
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

        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = NewTopic(name=[first_topic,Second_topic],num_partitions=4,replication_factor=2)
        admin.create_topics(topic_list)
    
    except Exception:
        pass
    
    try:
        IkaProducer(topic_name=first_topic, data=message_id,acks=acks).run()
    except Exception:
        pass
    
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        # consumer_timeout_ms=3000,                       # break connection if the consumer has fetched anything for 3 secs (e.g. in case of an empty topic)
        auto_offset_reset='earliest',                   # automatically reset the offset to the earliest offset (should the current offset be deleted or anything)
        enable_auto_commit=False,                        # offsets are committed automatically by the consumer
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        max_poll_records=100
    )
    consumer.subscribe([first_topic])
    logger.info('Consumer constructed')
    
    program_starts = time.time()
    
    try:
        while(True):
            now = time.time()
            logger.info("It has been {0} seconds since the loop started".format(now - program_starts))
            logger.info("About to call consumer.poll for new messages")
            msg = consumer.poll(0.1)
            for message in consumer:
                logger.info('Offset: %s', message.offset)
                messages_id = message.value
                print(messages_id)
                
                mail_df = pd.DataFrame.from_records(GmailCollecterModel("prod",transform_flag=transform_flag).collect_mail(user_id="me",
                                                                                                    message_id=messages_id,
                                                                                                    max_workers=max_workers),columns=["idMail","threadId","historyId","from","to","date","labelIds","spam","body","mimeType"]).to_json(orient="index")
                # return JSONResponse(content=mail_df)
                response = RedirectResponse(url='/redirected',data=mail_df)
                return response
        
        consumer.commit()
        logger.info("Offsets have been committed");
    
    except Exception:
        pass


@StreamProcess.get("/redirected")
async def redirected(data=None):
    logger.debug("debug message")
    Second_topic = 'gmail_corps'
    
    try:
        IkaProducer(topic_name=Second_topic, data=data,acks='all').run()
    except Exception:
        pass
    return {"message": "you've been redirected"}
