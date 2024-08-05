from django.urls import path
from . import views

urlpatterns = [
    path('kasko_detail/', views.kasko_detail, name='kasko_detail'),
    path('get_models/', views.get_models, name='get_models'),
    path('get_offer/', views.get_offer, name='get_offer'),
    path('payment/<int:police_id>/', views.payment, name='payment'),
    path('payment_success/<int:police_id>/', views.payment_success, name='payment_success'),
]

