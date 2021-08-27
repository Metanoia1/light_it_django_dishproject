import csv
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from dishproject.settings import BASE_DIR
from .utils import create_csv_report
from .models import Order


@shared_task
def report():
    with open(BASE_DIR / "report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        gt_date = now() - timedelta(days=1)
        queryset = Order.objects.all()
        create_csv_report(writer, gt_date, queryset)
