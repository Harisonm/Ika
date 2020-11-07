from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Response, request
from ika_web.app.api.database.models import Credential, User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from ika_web.app.api.resources.errors import SchemaValidationError, CredentialAlreadyExistsError, InternalServerError, \
UpdatingCredentialError, DeletingCredentialError, CredentialNotExistsError



class CredentialsApi(Resource):

    @jwt_required
    def get(self):
        """
        ---
        post:
        description: increments the input by x
        requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
        responses:
            '200':
            description: call successful
            content:
                application/json:
                schema: OutputSchema
        tags:
            - calculation
        """
        query = Credential.objects()
        credentials = Credential.objects().to_json()
        return Response(credentials, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        """
        ---
        post:
        description: increments the input by x
        requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
        responses:
            '200':
            description: call successful
            content:
                application/json:
                schema: OutputSchema
        tags:
            - calculation
        """
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get
            credential = Credential(**body, added_by=user)
            credential.save()
            user.update(push__credentials=Credential)
            user.save()
            id = credential.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise CredentialAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class CredentialApi(Resource):
    @jwt_required
    def put(self, id):
        """
        ---
        post:
        description: increments the input by x
        requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
        responses:
            '200':
            description: call successful
            content:
                application/json:
                schema: OutputSchema
        tags:
            - calculation
        """
        try:
            user_id = get_jwt_identity()
            credential = Credential.objects.get
            body = request.get_json()
            Credential.objects.get.update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingCredentialError
        except Exception:
            raise InternalServerError   

    @jwt_required
    def delete(self, id):
        """
        delete [summary]

        Args:
            id ([type]): [description]

        Raises:
            DeletingCredentialError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        try:
            user_id = get_jwt_identity()
            credential = Credential.objects.get
            credential.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingCredentialError
        except Exception:
            raise InternalServerError

    def get(self, id):
        """
        get [summary]

        Args:
            id ([type]): [description]

        Raises:
            CredentialNotExistsError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        try:
            credentials = Credential.objects.get.to_json()
            return Response(credentials, mimetype="application/json", status=200)
        except DoesNotExist:
            raise CredentialNotExistsError
        except Exception:
            raise InternalServerError
