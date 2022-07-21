from time import sleep
from celery import shared_task

@shared_task
def sleepy(duration):
    sleep(duration)
    return None