from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Response, request
from src.ika_web.app.api.database.models import Credential, User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from src.ika_web.app.api.resources.errors import SchemaValidationError, CredentialAlreadyExistsError, InternalServerError, \
UpdatingCredentialError, DeletingCredentialError, CredentialNotExistsError



class CredentialsApi(Resource):

    @jwt_required
    def get(self):
        """
        get [summary]

        Returns:
            [type]: [description]
        """
        query = Credential.objects()
        credentials = Credential.objects().to_json()
        return Response(credentials, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        """
        post [summary]

        Raises:
            SchemaValidationError: [description]
            CredentialAlreadyExistsError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
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
        put [summary]

        Args:
            id ([type]): [description]

        Raises:
            SchemaValidationError: [description]
            UpdatingCredentialError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        try:
            user_id = get_jwt_identity()
            credential = Credential.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Credential.objects.get(id=id).update(**body)
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
            credential = Credential.objects.get(id=id, added_by=user_id)
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
            credentials = Credential.objects.get(id=id).to_json()
            return Response(credentials, mimetype="application/json", status=200)
        except DoesNotExist:
            raise CredentialNotExistsError
        except Exception:
            raise InternalServerError
