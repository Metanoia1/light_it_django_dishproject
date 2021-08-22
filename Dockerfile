FROM python:3.8.11-slim

RUN apt update && apt install -y build-essential
# libpq-dev libmemcached-dev zlib1g-dev python3-dev gcc

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["bash", "/app/entrypoint.sh"]
