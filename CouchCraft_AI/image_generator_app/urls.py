from django.urls import path
from . import views


urlpatterns = [
    path("generate/", views.generate_image_view, name="generate_image"),
    path("previews/", views.generate_preview, name="generate_preview"),
    path('check-task/<str:task_id>/', views.check_task_view, name='check_task'),
]