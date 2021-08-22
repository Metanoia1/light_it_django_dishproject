FROM python:3.8.11-slim

RUN apt update && apt install -y build-essential

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["bash", "/app/entrypoint.sh"]
