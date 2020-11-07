"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title="Ika Web Connect",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# Define schemas
class InputSchema(Schema):
    number = fields.Int(description="An integer.", required=True)


class OutputSchema(Schema):
    msg = fields.String(description="A message.", required=True)


# register schemas with spec
spec.components.schema("Input", schema=InputSchema)
spec.components.schema("Output", schema=OutputSchema)

# add swagger tags that are used for endpoint annotation
tags = [
    {'name': 'testing',
     'description': 'For testing the API.'
     },
    {'name': 'Credentials',
     'description': 'Functions for credentials.'
     },
    {'name': 'auth',
     'description': 'Functions for Authentification in ika Web.'
     },
    {'name': 'google Gmail API',
     'description': 'Functions for using Gmail API.'
     },
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
