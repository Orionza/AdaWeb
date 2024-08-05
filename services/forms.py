from django import forms
from .models import AracBilgileri

class KaskoForm(forms.ModelForm):
    class Meta:
        model = AracBilgileri
        fields = ['plaka_il_kodu', 'plaka_kodu', 'arac_marka', 'arac_model_yili', 'arac_model']
