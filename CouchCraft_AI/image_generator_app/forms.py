from django import forms

MODEL_CHOICES = [
    ('realistic', 'Realistic Vision'),
    ('sd15', 'Stable Diffusion 1.5'),
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
        choices=MODEL_CHOICES
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

