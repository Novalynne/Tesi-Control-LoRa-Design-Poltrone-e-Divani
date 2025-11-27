from django.shortcuts import render
from .forms import TrainingForm

# Create your views here.

def training_view(request):
    job_id = None # Sostituisci con l'ID del job di training una volta avviato
    if request.method == "POST":
        form = TrainingForm(request.POST, request.FILES)

        if form.is_valid():
            # Qui invierai i dati a Celery + Lambda
            pass
    else:
        form = TrainingForm()

    return render(request, "train.html", {
        "form": form,
        "job_id": job_id,
    })

def training_status(request, job_id):
    # Qui controllerai lo stato del job di training
    pass