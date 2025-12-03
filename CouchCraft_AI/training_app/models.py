from django.db import models

# NO LONGER NEEDED: OUR TRAINING DOENS'T USE CELERY ANYMORE BECAUSE RUNPOD HANDLES ASYNC TRAINING

class TrainingJob(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=100)
    base_model = models.CharField(max_length=100)
    steps = models.IntegerField()
    rank = models.IntegerField()
    lr = models.FloatField()
    huggingFace_dataset = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="queued")
    step_done = models.IntegerField(default=0)  # step completati
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"
