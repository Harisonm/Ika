from src.web.app.resources.auth import SignupApi, LoginApi, CredentialsApi, CredentialApi

def initialize_routes(api):
    api.add_resource(CredentialsApi, '/api/credentials')
    api.add_resource(CredentialApi, '/api/credentials/<id>')
    
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    