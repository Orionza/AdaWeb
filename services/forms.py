from django import forms
from .models import AracBilgileri, DaskBilgileri 

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
