FROM python:3

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc libmemcached-dev zlib1g-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]
