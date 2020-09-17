#!/usr/bin/env bash
export FN_AUTH_REDIRECT_URI=http://127.0.0.1:8040/google/auth
export FN_BASE_URI=http://127.0.0.1:8040
export PORT_APP=8040
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=ika_web/app/app.py
export FLASK_DEBUG=1
export FLASK_ENV=production
# development
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET
export CLIENT_SECRET=ika_web/resources/client_secret_localhost.json
export ENV_FILE_LOCATION=./ika_web/app/.env.test
# code
export PATH_FILE=temp/
export HOME_URI=/home

# Database
export ENV_FILE_LOCATION=./.env
export MONGO_URI=mongodb://localhost:27017/ika
python -m flask run -p 8040 --host=127.0.0.1

# python -m flask run -p 8080 --host=0.0.0.0