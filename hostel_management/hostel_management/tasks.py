from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command  # NEW
import csv
from django.core.mail import EmailMessage
from io import StringIO
import datetime
import os
from django.utils.dateparse import parse_datetime

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def send_email_report():
    call_command(
        "email_report",
    )
