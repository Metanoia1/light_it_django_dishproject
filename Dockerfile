FROM python:3.8-slim

RUN apt update && apt install -y \
    gcc build-essential python3-dev libpq-dev libmemcached-dev zlib1g-dev python3-dev && \
    rm -rf /var/lib/apt/lists*

WORKDIR .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "createcachetable"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "dishproject.wsgi:application", "-b", "0.0.0.0:8000", "--reload", "-w", "4"]
