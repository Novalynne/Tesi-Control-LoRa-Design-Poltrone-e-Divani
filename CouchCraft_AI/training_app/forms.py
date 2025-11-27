from django import forms

BASE_MODELS = [
    ("SD 1.5 (runwayml)", "runwayml/stable-diffusion-v1-5"),
    ("Realistic Vision 4.0", "SG161222/Realistic_Vision_V4.0_noVAE"),
]

class TrainingForm(forms.Form):

    name = forms.CharField(label="Name of your LoRA task", max_length=128, required=True)

    base_model = forms.ChoiceField(
        label="Base Model",
        choices=BASE_MODELS
    )

    steps = forms.IntegerField(min_value=50, max_value=20000, initial=800)

    rank = forms.IntegerField(min_value=4, max_value=128, initial=16)

    lr = forms.FloatField(initial=1e-4, localize=True)

    huggingFace_dataset = forms.CharField(
        label="Public HuggingFace Dataset ID",
        max_length=128,
        help_text="Example: username/my-dataset",
        required=True
    )