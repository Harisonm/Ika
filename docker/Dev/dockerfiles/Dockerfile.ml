FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /home/4aibd-annuel-project

# Add requirements file
RUN pip install --upgrade pip
ADD requirements.ml.txt /app/
RUN pip install -r /app/requirements.ml.txt

#RUN curl -sSL https://sdk.cloud.google.com | bash

#ENV PATH $PATH:/root/google-cloud-sdk/bin
#CMD gcloud components update
#CMD gcloud init

EXPOSE 5000
EXPOSE 8000

#CMD mlflow server \
#    --host 0.0.0.0 \
#    --port=5000