from django import forms
from .models import AracBilgileri, DaskBilgileri 
from django.core.exceptions import ValidationError
import re

class KaskoForm(forms.ModelForm):
    class Meta:
        model = AracBilgileri
        fields = ['plaka_il_kodu', 'plaka_kodu', 'arac_marka', 'arac_model_yili', 'arac_model']

from django import forms
from .models import DaskBilgileri

class DaskForm(forms.ModelForm):
    class Meta:
        model = DaskBilgileri
        fields = ['bina_tipi', 'bina_yasi', 'kat_sayisi', 'bina_alani', 'risk_bolgesi']
        widgets = {
            'bina_tipi': forms.Select(attrs={'class': 'form-control'}),
            'bina_yasi': forms.NumberInput(attrs={'class': 'form-control'}),
            'kat_sayisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'bina_alani': forms.NumberInput(attrs={'class': 'form-control'}),
            'risk_bolgesi': forms.Select(attrs={'class': 'form-control'}),
        }

class AracBilgileriForm(forms.ModelForm):
    class Meta:
        model = AracBilgileri
        fields = '__all__'
    """
    def clean_plaka_il_kodu(self):
        plaka_il_kodu = self.cleaned_data.get('plaka_il_kodu')
        if not (10 <= plaka_il_kodu <= 99):
            raise forms.ValidationError("Plaka il kodu 2 basamaklı bir sayı olmalıdır.")
        return plaka_il_kodu

    def clean_plaka_kodu(self):
        plaka_kodu = self.cleaned_data.get('plaka_kodu')
        if not (plaka_kodu[:3].isalpha() and plaka_kodu[:3].isupper() and plaka_kodu[3:].isdigit() and len(plaka_kodu) == 5):
            raise forms.ValidationError("Plaka kodu 3 harf ve 2 rakamdan oluşmalıdır. Örneğin: ABC12")
        return plaka_kodu
    """

class PaymentForm(forms.Form):
    kredi_kart_no = forms.CharField(min_length=11, max_length=11, label='Kredi Kartı No')
    kredi_kart_sahibi = forms.CharField(label='Kredi Kartı Sahibi')
    son_kullanma_tarihi = forms.CharField(label='Son Kullanma Tarihi (MM/YY)')
    cvv = forms.CharField(min_length=3, max_length=3, label='CVV')

    def clean_son_kullanma_tarihi(self):
        data = self.cleaned_data['son_kullanma_tarihi']
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', data):
            raise forms.ValidationError("Son kullanma tarihi MM/YY formatında olmalıdır.")
        return data

    def clean_kredi_kart_no(self):
        data = self.cleaned_data['kredi_kart_no']
        if not data.isdigit() or len(data) != 11:
            raise forms.ValidationError("Kredi kartı numarası 11 haneli bir sayı olmalıdır.")
        return data

    def clean_cvv(self):
        data = self.cleaned_data['cvv']
        if not data.isdigit() or len(data) != 3:
            raise forms.ValidationError("CVV numarası 3 haneli bir sayı olmalıdır.")
        return data