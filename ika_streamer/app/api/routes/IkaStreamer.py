from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from ikamail.GmailHelper import GmailHelper
from app.api.models.CollecterModel import CollecterModel
from app.api.database.mongo import mdb
from app.api.models.Gmail import GmailOut
from bson.json_util import dumps
from typing import List
from pandas.io.json import json_normalize
from pandas import DataFrame
import pandas as pd

streamers = APIRouter()

@streamers.get('/')
async def create_stream(batch_using: bool=True, transform_flag: bool=True, include_spam_trash: bool=False, max_results:int=25, max_workers:int=25, file_return:str=None):
    """
    create_stream: 

    Args:
    
        batch_using (bool, optional): if Flag False -> Take nextPageToken else True -> Take by batch. Defaults to True.
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
        batch_using=batch_using
    )
    
    gmail_collection = mdb["streamer"]
    gmail_collection.insert(
                            CollecterModel("prod",
                                        transform_flag=transform_flag)
                            .collect_mail(user_id="me",
                                        message_id=message_id,
                                        max_workers=max_workers)
                            )
    
    response = gmail_collection.find_one()
    
    if not response:
        raise HTTPException(status_code=404, detail="Cast not found")
    
    if file_return is None:
        return RedirectResponse("http://127.0.0.1:8004/api/v1/classifier/labelling/build")
    
    elif file_return == 'csv':
            data = pd.DataFrame(list(gmail_collection.find()))
            compression_opts = dict(method='zip',
                            archive_name='out.csv')
            data.to_csv('gmail_file.zip', index=False,compression=compression_opts)  
            file_location='gmail_file.zip'
            return FileResponse(file_location, media_type='application/octet-stream',filename='gmail_file.zip')
        
    elif file_return == 'json':
        pass
    
@streamers.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
    
def write_in_db():
    pass 

def get_auth():
    pass