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
    if request.method == "POST" and request.FILES.get("image"):
        file = request.FILES["image"]

        # Convert file in array OpenCV
        img_array = np.frombuffer(file.read(), np.uint8)
        img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # ---- CANNY ----
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)

        # ---- HED ----
        img_pil = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        hed_map = hed_detector(img_pil)
        hed_np = np.array(hed_map.convert("L"))  # converti in numpy grayscale

        # ---- RESIZE se necessario ----
        if hed_np.shape != canny.shape:
            hed_np = cv2.resize(hed_np, (canny.shape[1], canny.shape[0]))

        # ---- COMBINAZIONE 50% / 50% ----
        combined = cv2.addWeighted(canny.astype(np.float32), 0.5, hed_np.astype(np.float32), 0.5, 0)

        combined = combined.astype(np.uint8)

        # ---- Output base64 ----
        _, buffer = cv2.imencode(".png", combined)
        combined_b64 = base64.b64encode(buffer).decode()

        return JsonResponse({
            "status": "ok",
            "combined": f"data:image/png;base64,{combined_b64}"
        })

    return JsonResponse({"status": "error", "message": "Missing file"}, status=400)


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

