FROM python:3.9-slim 

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN apt-get update -y && apt-get -y install wkhtmltopdf 

COPY . /app

RUN pip install -r requirements.txt



RUN chmod +x /app/server.sh \
    && chmod +x /app/worker.sh


