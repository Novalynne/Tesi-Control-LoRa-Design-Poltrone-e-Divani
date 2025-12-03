from io import BytesIO

from django.shortcuts import render
from .forms import ImageGenerationForm
import cv2
import numpy as np
import base64
import requests
from django.http import JsonResponse
from controlnet_aux.hed import HEDdetector
from PIL import Image
import tempfile
from django.shortcuts import render


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

POD_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/generate"  # URL del tuo pod

def generate_image_view(request):
    generated_image_base64 = None  # Base64 dell'immagine generata

    if request.method == "POST":
        form = ImageGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            canvas_base64 = request.POST.get("canvasEdited")
            if canvas_base64:
                try:
                    # ---- Decodifica base64 inviato dal canvas ----
                    format, imgstr = canvas_base64.split(";base64,")
                    image_bytes = base64.b64decode(imgstr)
                    canvas_file = BytesIO(image_bytes)
                    canvas_file.name = "canvas.png"

                    # ---- Prepara dati da inviare al pod ----
                    files = {"canvas_image": ("canvas.png", canvas_file, "image/png")}
                    data = {
                        "prompt": form.cleaned_data["prompt"],
                        "negative_prompt": form.cleaned_data.get("negative_prompt", ""),
                        "model_choice": form.cleaned_data["model_choice"],
                        "lora_weight": form.cleaned_data["lora_weight"],
                        "guidance_scale": form.cleaned_data["guidance_scale"],
                        "conditioning_scale": form.cleaned_data["conditioning_scale"],
                        "num_steps": form.cleaned_data["num_steps"],
                    }

                    # ---- Chiamata diretta al pod RunPod ----
                    response = requests.post(POD_URL, data=data, files=files)
                    response.raise_for_status()
                    result = response.json()

                    # ---- Prendi Base64 dell'immagine generata ----
                    img_base64 = result.get("image_base64")
                    if img_base64:
                        generated_image_base64 = img_base64

                except Exception as e:
                    return render(request, "generate_image.html", {
                        "form": form,
                        "error_message": f"Errore durante la generazione: {e}",
                        "generated_image_base64": None
                    })
    else:
        form = ImageGenerationForm()

    # ---- Render template con immagine (Base64) ----
    return render(request, "generate_image.html", {
        "form": form,
        "generated_image_base64": generated_image_base64
    })
