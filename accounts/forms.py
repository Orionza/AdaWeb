from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['Id_No', 'first_name', 'last_name', 'city', 'district', 'phone', 'email', 'password1', 'password2']
        labels = {
            'Id_No': 'Kimlik Numarası', 
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'city': 'Şehir',
            'district': 'İlçe',
            'phone': 'Telefon',
            'email': 'E-posta',
            'password1': 'Parola',
            'password2': 'Parola (Tekrar)',
        }

    def clean_Id_No(self):
        Id_No = self.cleaned_data.get('Id_No')
        if len(Id_No) != 11 or not Id_No.isdigit():
            raise ValidationError('Kimlik numarası 11 haneli bir sayı olmalıdır.')
        return Id_No

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError('Ad kısmı sadece harflerden oluşmalıdır.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError('Soyad kısmı sadece harflerden oluşmalıdır.')
        return last_name

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city.isalpha():
            raise ValidationError('Şehir kısmı sadece harflerden oluşmalıdır.')
        return city

    def clean_district(self):
        district = self.cleaned_data.get('district')
        if not district.isalpha():
            raise ValidationError('İlçe kısmı sadece harflerden oluşmalıdır.')
        return district

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10 or not phone.isdigit():
            raise ValidationError('Telefon numarası 10 haneli bir sayı olmalıdır.')
        return phone
