from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine.fields import StringField

class Credential(db.Document):
    token = db.StringField(required=True, unique=False)
    refresh_token = db.StringField(required=True, unique=False)
    token_uri = db.StringField(required=True, unique=False)
    client_id = db.StringField(required=True, unique=False)
    client_secret = db.StringField(required=True, unique=False)
    scopes = db.ListField(StringField(max_length=300))
   #added_by = db.ReferenceField('User')


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    first_name = db.StringField(required=False, unique=False)
    last_name = db.StringField(required=False, unique=False)
    password = db.StringField(required=True, min_length=6)
    ##credentials = db.ListField(db.ReferenceField('Credential', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


User.register_delete_rule(Credential, 'added_by', db.CASCADE)
