from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from ikamail.GmailHelper import GmailHelper
from app.api.models.CollecterModel import CollecterModel
from app.api.database.mongo import mdb
from app.api.models.Gmail import GmailOut
from typing import List

streamers = APIRouter()

@streamers.get('/', response_model=GmailOut)
async def create_streamer(batch_using: bool=True,
                          transform_flag: bool=True,
                          include_spam_trash: bool=False,
                          max_results:int=25,
                          max_workers:int=25):
    
    message_id = GmailHelper("prod").get_message_id(
        "me",
        include_spam_trash=include_spam_trash,
        max_results=max_results,
        batch_using=batch_using
    )
    
    mycol = mdb["streamer"]
    mycol.insert(CollecterModel("prod",
                                transform_flag=transform_flag).collect_mail(user_id="me",
                                                                   message_id=message_id,
                                                                   max_workers=max_workers))
    response = mycol.find_one()
    
    if not response:
        raise HTTPException(status_code=404, detail="Cast not found")
    
    # Test
    return RedirectResponse("http://127.0.0.1:5000/api/v1/labelling/")
    

def write_in_csv():
    pass

def write_in_json():
    pass 

def write_in_db():
    pass 

def get_auth():
    pass