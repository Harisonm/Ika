from .db import db

class Credential(db.Document):
    token = db.StringField(required=True, unique=True)
    refresh_token = db.StringField(required=True, unique=True)
    token_uri = db.StringField(required=True, unique=True)
    client_id = db.StringField(required=True, unique=True)
    client_secret = db.StringField(required=True, unique=True)
    scopes = db.StringField(required=False, unique=True)