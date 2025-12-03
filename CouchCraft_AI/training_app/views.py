from django.shortcuts import render, redirect
import threading, requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TrainingJob
from .forms import TrainingForm
import time


# Create your views here.

RUNPOD_TRAIN_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/train"

def training_view(request):
    training_started = False
    hf_url = ""

    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "base_model": form.cleaned_data['base_model'],
                "steps": form.cleaned_data['steps'],
                "rank": form.cleaned_data['rank'],
                "lr": form.cleaned_data['lr'],
                "huggingFace_dataset": form.cleaned_data['huggingFace_dataset'],
                "hub_model_id": form.cleaned_data['hub_model_id'],
                "hub_token": form.cleaned_data['hub_token'],
            }

            # POST al server RunPod AI
            r = requests.post(RUNPOD_TRAIN_URL, data=data)
            if r.status_code == 200:
                training_started = True
                hf_url = r.json().get("hf_url", "#")

    else:
        form = TrainingForm()

    return render(request, "train.html", {
        "form": form,
        "training_started": training_started,
        "hf_url": hf_url,
    })