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
export SCHEMA_COLLECT=src/app/collect_mail/resources/schema/gmail_fields.json
export PATH_SAVE_COLLECT=a_collect_gmail/
export SCHEMA_TRANSFORM=src/app/transform_mail/resources/schema/gmail_fields.json
export PATH_SAVE_TRANSFORM=b_transform_gmail/
export HOME_URI=/home

python -m flask run -p 8040 --host=127.0.0.1