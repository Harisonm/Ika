from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from ikamail.GmailHelper import GmailHelper
from app.api.models.CollecterModel import CollecterModel
from app.api.database.mongo import mdb
from app.api.models.Gmail import GmailOut
from typing import List

streamers = APIRouter()

@streamers.get('/', response_model=GmailOut)
async def create_streamer():
    
    message_id = GmailHelper("prod").get_message_id(
        "me",
        include_spam_trash=False,
        max_results=25,
        batch_using=False
    )
    
    mycol = mdb["streamer"]
    mycol.insert(CollecterModel("prod",
                                transform_flag=False).collect_mail(user_id="me",
                                                                message_id=message_id,
                                                                max_workers=25))
    response = mycol.find_one()
    
    if not response:
        raise HTTPException(status_code=404, detail="Cast not found")
    
    # Test
    return RedirectResponse("http://127.0.0.1:5000/api/v1/labelling/")
    

def get_auth():
    pass