from django.urls import path
from . import views


urlpatterns = [
    path('train/', views.training_view, name='training_view'),
]