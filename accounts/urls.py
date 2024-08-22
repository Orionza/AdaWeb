from django.urls import path
from . import views
from services.views import payment, payment_success

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('', views.home, name='home'),  
    path('kasko_detail/', views.kasko_detail, name='kasko_detail'), 
    path('iptal_et/<int:police_id>/', views.iptal_et, name='iptal_et'),  
    path('payment/<int:police_id>/', payment, name='payment'),  # Burada services.views'den gelen payment fonksiyonu kullanılıyor
    path('payment_success/<int:police_id>/', payment_success, name='payment_success'),  # Aynı şekilde
]
#son