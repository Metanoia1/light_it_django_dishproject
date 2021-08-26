FROM python:3.8.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3-dev libpq-dev gcc libmemcached-dev zlib1g-dev build-essential

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
