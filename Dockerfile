FROM python:3.8-slim

RUN useradd -u 8877 john

USER john

RUN apt update && apt install -y \
    build-essential libpq-dev libmemcached-dev zlib1g-dev python3-dev gcc && \
    rm -rf /var/lib/apt/lists*

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "dishproject.wsgi:application", "-b", "0.0.0.0:8000", "--reload", "-w", "4"]
