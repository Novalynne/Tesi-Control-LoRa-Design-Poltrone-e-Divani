from django.urls import path
from . import views


urlpatterns = [
    path('train/', views.training_view, name='training_view'),
    path("status/<uuid:job_id>/", views.training_status, name="status"),
]