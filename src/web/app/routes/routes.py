from src.web.app.resources.login import SignupApi, LoginApi
from src.web.app.resources.credential import CredentialsApi, CredentialApi

def initialize_routes(api):
    api.add_resource(CredentialsApi, '/api/v1/credentials')
    api.add_resource(CredentialApi, '/api/v1/credentials/<id>')
    
    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')

    