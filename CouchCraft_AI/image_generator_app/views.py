from django.shortcuts import render
from .forms import ImageGenerationForm
import cv2
import numpy as np
import base64
from django.http import JsonResponse
from controlnet_aux.hed import HEDdetector
from PIL import Image

# CARICAMENTO MODEL HED
hed_detector = HEDdetector.from_pretrained("lllyasviel/Annotators")


# Create your views here.
def generate_preview(request):
    if request.method != "POST" or not request.FILES.get("image"):
        return JsonResponse({"status": "error", "message": "Missing file"}, status=400)

    file = request.FILES["image"]

    # ---- CARICAMENTO IMMAGINE ----
    try:
        image = Image.open(file)
        image = image.convert("RGB")  # assicura 3 canali
        img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Impossibile leggere l'immagine: {e}"}, status=400)

    # ---- CANNY ----
    try:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Errore Canny: {e}"}, status=500)

    # ---- HED ----
    try:
        img_pil = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        hed_map = hed_detector(img_pil)
        hed_np = np.array(hed_map.convert("L"))  # grayscale numpy
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Errore HED: {e}"}, status=500)

    # ---- RESIZE HED se necessario ----
    if hed_np.shape != canny.shape:
        hed_np = cv2.resize(hed_np, (canny.shape[1], canny.shape[0]))

    # ---- COMBINAZIONE 50% / 50% ----
    combined = cv2.addWeighted(canny.astype(np.float32), 0.5, hed_np.astype(np.float32), 0.5, 0)
    combined = combined.astype(np.uint8)

    # ---- OUTPUT BASE64 ----
    _, buffer = cv2.imencode(".png", combined)
    combined_b64 = base64.b64encode(buffer).decode()

    return JsonResponse({
        "status": "ok",
        "combined": f"data:image/png;base64,{combined_b64}"
    })


def generate_image_view(request):
    hed_preview_url = None  # poi lo userai per mostrare la canny/HED

    if request.method == "POST":
        form = ImageGenerationForm(request.POST, request.FILES)

        if form.is_valid():
            # Qui invierai i dati a Celery + Lambda
            pass
    else:
        form = ImageGenerationForm()

    return render(request, "generate_image.html", {
        "form": form,
        "hed_preview_url": hed_preview_url
    })

