import requests
import base64
from io import BytesIO
from celery import shared_task

POD_URL = "https://ga4nj7qaxm1hu4-3000.proxy.runpod.net/generate"

@shared_task
def generate_image_task(data, canvas_base64):
    """
    Esegue la generazione immagine su Runpod.
    """
    try:
        # Decodifica immagine
        format, imgstr = canvas_base64.split(";base64,")
        image_bytes = base64.b64decode(imgstr)
        canvas_file = BytesIO(image_bytes)
        canvas_file.name = "canvas.png"

        files = {"canvas_image": ("canvas.png", canvas_file, "image/png")}

        response = requests.post(POD_URL, data=data, files=files)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("status") == "success" and "image_base64" in response_data:
            return {"status": "success", "image_base64": response_data["image_base64"]}
        else:
            return {"status": "error", "error": response_data.get("error", "Unknown error")}
    except Exception as e:
        return {"status": "error", "error": str(e)}
