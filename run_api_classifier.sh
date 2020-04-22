#!/usr/bin/env bash
export FN_BASE_URI=http://127.0.0.1:5000
export PORT_APP=5000
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=src/app/ika_classifier/app.py
export FLASK_DEBUG=1
export FLASK_ENV=production
# development
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET

# code
export PATH_FILE=temp/
export HOME_URI=/home

# Database
export MONGO_URI=mongodb://localhost:27017/
export GOOGLE_GMAIL_URI=https://mail.google.com/mail/u/0/#inbox

python -m flask run -p 5000 --host=127.0.0.1

# python -m flask run -p 8080 --host=0.0.0.0