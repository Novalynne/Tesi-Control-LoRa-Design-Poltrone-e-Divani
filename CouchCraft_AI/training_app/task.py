import requests
import base64
from io import BytesIO
from celery import shared_task

RUNPOD_TRAIN_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/train"


@shared_task
def run_training_task(data):
    """
    Esegue la chiamata di training a Runpod.
    """
    r = requests.post(RUNPOD_TRAIN_URL, data=data)
    if r.status_code == 200:
        return r.json()
    return {"error": f"Training failed with status {r.status_code}"}
