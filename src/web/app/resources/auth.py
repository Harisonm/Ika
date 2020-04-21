from flask import Response, request
from flask_jwt_extended import create_access_token
from src.web.database.models import Credential,User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import datetime

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user =  User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200

# Class pour le credential
class CredentialsApi(Resource):
    def get(self):
        query = Credential.objects()
        credentials = Credential.objects().to_json()
        return Response(credentials, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id=user_id)
        credential = Credential(**body, added_by=user)
        credential.save()
        user.update(push__credentials=Credential)
        user.save()
        id = credential.id
        return {'id': str(id)}, 200

class CredentialApi(Resource):
    @jwt_required
    def put(self, id):
        user_id = get_jwt_identity()
        credential = Credential.objects.get(id=id, added_by=user_id)
        body = request.get_json()
        Credential.objects.get(id=id).update(**body)
        return '', 200
    
    @jwt_required
    def delete(self, id):
        user_id = get_jwt_identity()
        credential = Credential.objects.get(id=id, added_by=user_id)
        credential.delete()
        return '', 200

    def get(self, id):
        credentials = Credential.objects.get(id=id).to_json()
        return Response(credentials, mimetype="application/json", status=200)
