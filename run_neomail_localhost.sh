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
export SERVICE_ACCOUNT_GCP=resources/gcp_credential/service_account.json

python -m flask run -p 8040 --host=127.0.0.1

# Client ID = 733410412587-k0lbh0marnut2skv5ou6c797p60fk5u3.apps.googleusercontent.com
# Client secret = o7ziQIa3CFghx3K7VSylGGnb