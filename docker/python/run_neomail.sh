#!/usr/bin/env bash
export FN_AUTH_REDIRECT_URI=http://127.0.0.1:8040/google/auth
export FN_BASE_URI=http://127.0.0.1:8040
export PORT_APP=8040
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=src/web/app.py
export FLASK_DEBUG=1
export FLASK_ENV=development
# development
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET

export CLIENT_SECRETS_FILE=resources/api_gcp_credential/client_secret_localhost.json
export CLIENT_SECRET=resources/gmail_credential/gmail_credentials.json
export SERVICE_ACCOUNT_GCP=resources/gcp_credential/service_account.json

# code
export PATH_FILE=temp/
export HOME_URI=/home

# schema
export SCHEMA_COLLECT=src/api/collecter_mail/resources/schema/gmail_fields.json
export SCHEMA_TRANSFORM=src/api/transformer_mail/resources/schema/gmail_fields.json

python -m flask run -p 8040 --host=127.0.0.1
# python -m flask run -p 8080 --host=0.0.0.0