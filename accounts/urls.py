from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('', views.home, name='home'),  # Ana sayfa URL'i buraya taşındı
    path('kasko_detail/', views.kasko_detail, name='kasko_detail'),
]

