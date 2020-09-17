import datetime

from flask import request, render_template
from flask_restful import Resource
from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, DecodeError, \
    InvalidTokenError
from src.ika_web.app.api.database.models import User
from src.ika_web.app.api.resources.errors import SchemaValidationError, InternalServerError, \
    EmailDoesnotExistsError, BadTokenError
from src.ika_web.app.api.services.mail_service import send_email


class ForgotPassword(Resource):
    def post(self):
        """
        post [summary]

        Raises:
            SchemaValidationError: [description]
            EmailDoesnotExistsError: [description]
            SchemaValidationError: [description]
            EmailDoesnotExistsError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError

            user = User.objects.get(email=email)
            if not user:
                raise EmailDoesnotExistsError

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.id), expires_delta=expires)
            
            return send_email('[Credential] Reset Your Password',
                              sender='support@ika.com',
                              recipients=[user.email],
                              text_body=render_template('reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('reset_password.html',
                                                        url=url + reset_token))
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailDoesnotExistsError:
            raise EmailDoesnotExistsError
        except Exception as e:
            raise InternalServerError


class ResetPassword(Resource):
    def post(self):
        """
        post [summary]

        Raises:
            SchemaValidationError: [description]
            SchemaValidationError: [description]
            ExpiredTokenError: [description]
            BadTokenError: [description]
            InternalServerError: [description]

        Returns:
            [type]: [description]
        """
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['identity']

            user = User.objects.get(id=user_id)

            user.modify(password=password)
            user.hash_password()
            user.save()

            return send_email('[Credential] Password reset successful',
                              sender='support@ika.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError:
            raise SchemaValidationError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError