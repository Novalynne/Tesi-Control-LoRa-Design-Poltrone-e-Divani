from django.urls import path
from . import views


urlpatterns = [
    path("generate/", views.generate_image_view, name="generate_image"),
    path("previews/", views.generate_preview, name="generate_preview"),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
]