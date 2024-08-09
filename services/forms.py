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

    BINA_TIPI_CHOICES = [
        ('Betonarme', 'Betonarme'),
        ('Çelik', 'Çelik'),
        ('Ahşap', 'Ahşap'),
        ('Yığma', 'Yığma'),
    ]

    RISK_BOLGESI_CHOICES = [
        ('1', 'Bölge 1 (En yüksek risk)'),
        ('2', 'Bölge 2'),
        ('3', 'Bölge 3'),
        ('4', 'Bölge 4'),
    ]

    bina_tipi = forms.ChoiceField(choices=BINA_TIPI_CHOICES)
    risk_bolgesi = forms.ChoiceField(choices=RISK_BOLGESI_CHOICES)
