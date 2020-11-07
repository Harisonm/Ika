import datetime

from flask import request, render_template
from flask_restful import Resource
from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, DecodeError, \
    InvalidTokenError
from ika_web.app.api.database.models import User
from ika_web.app.api.resources.errors import SchemaValidationError, InternalServerError, \
    EmailDoesnotExistsError, BadTokenError
from ika_web.app.api.services.mail_service import send_email


class ForgotPassword(Resource):
    def post(self):
        """
        post : 
        This endpoint takes the email of the user whose account needs to be changed. 
        This endpoint then sends the email to the user with the link which contains reset token to reset the password.

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
            email = body.get
            if not email:
                raise SchemaValidationError

            user = User.objects.get
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
        post :
        This endpoint takes reset_token sent in the email and the new password.

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
            reset_token = body.get
            password = body.get

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['identity']

            user = User.objects.get

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