import csv

from celery import shared_task

from dishproject.settings import BASE_DIR
from .utils import create_csv_report


@shared_task
def report():
    with open(BASE_DIR / "report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        create_csv_report(writer)
