from src.app.ika_streamer.api.helper.GmailHelper import GmailDataFactory
from src.app.ika_streamer.api.models.CollecterModel import CollecterModel
from src.app.ika_streamer.api.database.mongo import mdb
from fastapi import APIRouter, HTTPException
from src.app.ika_streamer.api.models.Gmail import Gmail
from typing import List
import json
import csv
import os
import time

# SCHEMA_TRANSFORM = os.environ.get("SCHEMA_TRANSFORM", default=False)
# SCHEMA_COLLECT = os.environ.get("SCHEMA_COLLECT", default=False)
# PATH_SAVE = os.environ.get("PATH_FILE", default=False)
# HOME_URI = os.environ.get("HOME_URI", default=False)

streamers = APIRouter()

@streamers.get('/', response_model=Gmail, status_code=201)
async def create_streamer():
    
    message_id = GmailDataFactory("prod").get_message_id(
        "me",
        include_spam_trash=False,
        max_results=25,
        batch_using=False
    )
    
    mycol = mdb["streamer"]
    large_generator_handle = CollecterModel("prod",
                                            transform_flag=True).collect_mail(user_id="me",
                                                                              message_id=message_id,
                                                                              max_workers=25)
                                            
    mycol.insert(large_generator_handle)
    response = mycol.find_one()
    
    if not response:
        raise HTTPException(status_code=404, detail="Cast not found")
    return response
    


