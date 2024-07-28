from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),  
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('logout/', views.logout_view, name='logout'),

]
