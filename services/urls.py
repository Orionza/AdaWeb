from django.urls import path
from . import views

urlpatterns = [
    path('kasko_detail/', views.kasko_detail, name='kasko_detail'),
    path('get_models/', views.get_models, name='get_models'),
    path('get_offer/', views.get_offer, name='get_offer'),
    path('payment/<int:police_id>/', views.payment, name='payment'),
    path('payment_success/<int:police_id>/', views.payment_success, name='payment_success'),
    path('health/', views.health_insurance, name='health_insurance'),
    path('health/offer/', views.get_health_offer, name='get_health_offer'),
    path('plan/select/<int:plan_id>/', views.plan_select, name='plan_select'),
    path('dask_detail/', views.dask_detail, name='dask_detail'),
]
