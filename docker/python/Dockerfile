FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requierments.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requierments.txt
COPY . /code/
WORKDIR /home
COPY run_neomail.sh /home/
