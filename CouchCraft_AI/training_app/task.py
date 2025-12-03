import time
import requests
from celery import shared_task
from .models import TrainingJob

# NO LONGER NEEDED: OUR TRAINING DOENS'T USE CELERY ANYMORE BECAUSE RUNPOD HANDLES ASYNC TRAINING

RUNPOD_TRAIN_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/train"
RUNPOD_STATUS_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/status/"

@shared_task(bind=True)
def start_training(self, job_id, name, base_model, steps, rank, lr, huggingFace_dataset):
    job = TrainingJob.objects.get(id=job_id)
    job.status = "running"
    job.save()

    data = {
        "name": name,
        "base_model": base_model,
        "steps": steps,
        "rank": rank,
        "lr": lr,
        "huggingFace_dataset": huggingFace_dataset
    }

    try:
        # 1️⃣ Avvia training sul pod
        print(f"[Celery] Sending training request to pod for job {name}")
        r = requests.post(RUNPOD_TRAIN_URL, data=data)
        print(f"[Celery] Response: {r.status_code}, {r.text}")
        if r.status_code != 200:
            job.status = "failed"
            job.save()
            return

        # 2️⃣ Polling sullo stato finché non finisce
        while True:
            status_resp = requests.get(f"{RUNPOD_STATUS_URL}{name}")
            status_data = status_resp.json()
            job.status = status_data.get("status", job.status)
            job.step_done = status_data.get("step", 0)
            job.save()

            if job.status in ["completed", "failed"]:
                break
            time.sleep(5)  # controlla ogni 5 secondi

    except Exception as e:
        job.status = "failed"
        job.save()
