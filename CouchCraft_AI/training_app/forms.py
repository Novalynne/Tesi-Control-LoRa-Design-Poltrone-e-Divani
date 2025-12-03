from django import forms

BASE_MODELS = [
    ("SG161222/Realistic_Vision_V4.0_noVAE", "Realistic Vision 4.0"),
    ("runwayml/stable-diffusion-v1-5", "Stable Diffusion 1.5"),
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

    hub_token = forms.CharField(
        label="HuggingFace Token To Push Model",
        max_length=128,
        widget=forms.PasswordInput,
        required=True
    )

    hub_model_id = forms.CharField(
        label="HuggingFace Model Id to Push",
        max_length=128,
        help_text="Example: username/my-lora-model",
        required=True
    )
