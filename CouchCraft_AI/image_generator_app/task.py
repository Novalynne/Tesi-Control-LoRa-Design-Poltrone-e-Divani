# app/tasks.py
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from celery import shared_task
import base64
from io import BytesIO

@shared_task
def generate_image_task(canvas_base64, prompt, negative_prompt, model_choice, lora_weight, guidance_scale, conditioning_scale, num_steps):
    pod_url = "http://213.192.2.84:3000/generate"

    try:
        # Decodifica canvas inviato dall'utente
        format, imgstr = canvas_base64.split(";base64,")
        image_bytes = base64.b64decode(imgstr)
        canvas_file = BytesIO(image_bytes)
        canvas_file.name = "canvas.png"

        files = {"canvas_image": ("canvas.png", canvas_file, "image/png")}
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "model_choice": model_choice,
            "lora_weight": lora_weight,
            "guidance_scale": guidance_scale,
            "conditioning_scale": conditioning_scale,
            "num_steps": num_steps,
        }

        # Chiamata POST al pod
        response = requests.post(pod_url, data=data, files=files)
        response.raise_for_status()
        result = response.json()

        img_base64 = result.get("image_base64")
        if img_base64:
            img_bytes = base64.b64decode(img_base64)
            filename = f"generated/generated_image.png"
            saved_path = default_storage.save(filename, ContentFile(img_bytes))
            return default_storage.url(saved_path)

    except Exception as e:
        print("Errore Celery generate_image_task:", e)

    return None
