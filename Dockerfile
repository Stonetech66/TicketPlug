FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update -y && apt-get -y install wkhtmltopdf 

COPY . /app/

RUN chmod +x server.sh && chmod +x worker.sh



