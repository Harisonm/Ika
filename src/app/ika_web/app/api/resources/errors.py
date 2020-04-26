#~/movie-bag/resources/errors.py

class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class CredentialAlreadyExistsError(Exception):
    pass

class UpdatingCredentialError(Exception):
    pass

class DeletingCredentialError(Exception):
    pass

class CredentialNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "CredentialAlreadyExistsError": {
         "message": "Credential with given name already exists",
         "status": 400
     },
     "UpdatingCredentialError": {
         "message": "Updating credential added by other is forbidden",
         "status": 403
     },
     "DeletingCredentialError": {
         "message": "Deleting movie added by other is forbidden",
         "status": 403
     },
     "CredentialNotExistsError": {
         "message": "Credential with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     }
}