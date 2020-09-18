"""Definition of the Swagger UI Blueprint."""

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/v1/docs'
API_URL = "/api/v1/swagger.json"

# Call factory function to create our blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Ika Web Connect"
    }
)