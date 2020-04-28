FROM python:3.8-slim

WORKDIR /ika_web

COPY requirements.txt /ika_web/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /ika_web/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /ika_web/