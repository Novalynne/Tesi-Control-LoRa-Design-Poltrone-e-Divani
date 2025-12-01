from django import forms

MODEL_CHOICES = [
    ("SG161222/Realistic_Vision_V4.0_noVAE", "Realistic Vision 4.0"),
    ("runwayml/stable-diffusion-v1-5", "Stable Diffusion 1.5"),
]

class ImageGenerationForm(forms.Form):
    input_image = forms.ImageField(label="Upload Image")

    prompt = forms.CharField(
        label="Prompt",
        required=True,
        widget=forms.Textarea(attrs={"rows": 3})
    )

    negative_prompt = forms.CharField(
        label="Negative Prompt",
        widget=forms.Textarea(attrs={"rows": 2}),
        required=True,
        initial="deformed, distorted, sketch, blurry, cartoon, colored background"
    )

    model_choice = forms.ChoiceField(
        label="Model",
        choices=MODEL_CHOICES,
        required=True
    )

    lora_weight = forms.CharField(
        label="LoRA Weights (Public on HuggingFace)",
        required=True,
        initial="urllamadrama/furniture_control_lora_realistic_vision",
        help_text="Format: ursername/lora_weight_name"
    )

    guidance_scale = forms.FloatField(
        label="Guidance Scale",
        min_value=0, max_value=20, initial=6
    )

    conditioning_scale = forms.FloatField(
        label="Conditioning Scale",
        min_value=0, max_value=20, initial=0.7
    )

    num_steps = forms.IntegerField(
        label="Number of Steps",
        min_value=1, max_value=150, initial=20
    )

