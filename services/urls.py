from django.urls import path
from . import views

urlpatterns = [
    path('kasko_detail/', views.kasko_detail, name='kasko_detail'),
]
