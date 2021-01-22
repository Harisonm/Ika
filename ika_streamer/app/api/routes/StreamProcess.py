from fastapi import APIRouter, HTTPException, Request, FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from starlette.responses import FileResponse
from ikamail.GmailHelper import GmailHelper
from app.api.models.Gmail.GmailCollecterModel import GmailCollecterModel
from app.api.models.Consumer.IkaConsumer import IkaConsumer
from app.api.models.Producer.IkaProducer import IkaProducer
from app.api.models.Gmail.GmailSchema import GmailOut
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


KAFKA_URI=os.environ.get("KAFKA_URI", default=False)

GmailStreamers = APIRouter()
                
@GmailStreamers.get('/BuildMail')
async def BuildMail(batch_using: bool=True, transform_flag: bool=True, include_spam_trash: bool=False, max_results:int=200, max_workers:int=100, file_return:str=None):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}