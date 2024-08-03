from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['Id_No', 'first_name', 'last_name', 'city', 'district', 'phone', 'email', 'password1', 'password2']
        labels = {
            'Id_No': 'ID Number', 
        }

