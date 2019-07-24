#!/usr/bin/env bash
export FN_AUTH_REDIRECT_URI=http://beta.neomail.online:8080/google/auth
export FN_BASE_URI=http://beta.neomail.online:8080
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=default/components/o_auth2_web_server/app.py
export FLASK_DEBUG=1
export FLASK_ENV=production
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET
export CLIENT_SECRETS_FILE=resources/api_gcp_credential/client_secret.json
export SERVICE_ACCOUNT_GCP=resources/gcp_credential/service_account.json

python -m flask run -p 8080 --host=0.0.0.0
