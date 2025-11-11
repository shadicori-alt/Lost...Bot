# tasks/tasks.py
from celery import Celery
from services.notifier import send_daily_report
from services.shopify_sync import sync_products

celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))

@celery.task
def daily_report_task():
    send_daily_report()

@celery.task
def sync_products_task():
    sync_products()
