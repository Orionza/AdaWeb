from django.db import models
from django.conf import settings
import random
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Police(models.Model):
    POLICE_STATUS_CHOICES = [
        ('T', 'Teklif'),
        ('P', 'Poliçeleşmiş')
    ]

    police_no = models.IntegerField(unique=True)
    musteri_no = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=POLICE_STATUS_CHOICES, null= False, blank= False)
    brans_kodu = models.CharField(max_length=3)
    prim = models.DecimalField(max_digits=10, decimal_places=2)
    onaylayan = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='onaylayan', on_delete=models.CASCADE)
    tanzim_tarihi = models.DateTimeField(auto_now_add=True)
    baslangic_tarihi = models.DateTimeField()
    bitis_tarihi = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Poliçeler'

    def __str__(self):
        return str(self.police_no)

    def save(self, *args, **kwargs):
        if not self.police_no:
            self.police_no = self.generate_unique_police_no()
        super().save(*args, **kwargs)

    def generate_unique_police_no(self):
        while True:
            police_no = random.randint(10000000, 99999999)
            if not Police.objects.filter(police_no=police_no).exists():
                return police_no

class AracBilgileri(models.Model):
    police_no = models.OneToOneField(Police, on_delete=models.CASCADE)
    plaka_il_kodu = models.IntegerField()
    plaka_kodu = models.CharField(max_length=7)
    arac_marka = models.CharField(max_length=255)
    arac_model = models.CharField(max_length=255)
    arac_model_yili = models.IntegerField()
    motor_no = models.CharField(max_length=15)
    sasi_no = models.CharField(max_length=17)
    teklif_fiyati = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Araç Poliçe Bilgileri'

    def __str__(self):
        return f"{self.police_no.police_no} - {self.plaka_kodu}"
        

class OdemeBilgileri(models.Model):
    police_no = models.OneToOneField(Police, on_delete=models.CASCADE)
    odeme_tutari = models.DecimalField(max_digits=10, decimal_places=2)
    odeme_tarihi = models.DateTimeField(auto_now_add=True)
    kredi_kart_no = models.CharField(max_length=16)
    kredi_kart_sahibi = models.CharField(max_length=100)
    son_kullanma_tarihi = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'Ödeme Bilgileri'

class Vehicle(models.Model):
    marka_kodu = models.IntegerField()
    tip_kodu = models.IntegerField()
    marka_adi = models.CharField(max_length=255)
    tip_adi = models.CharField(max_length=255)
    model_2024 = models.IntegerField()
    model_2023 = models.IntegerField()
    model_2022 = models.IntegerField()
    model_2021 = models.IntegerField()
    model_2020 = models.IntegerField()
    model_2019 = models.IntegerField()
    model_2018 = models.IntegerField()
    model_2017 = models.IntegerField()
    model_2016 = models.IntegerField()
    model_2015 = models.IntegerField()
    model_2014 = models.IntegerField()
    model_2013 = models.IntegerField()
    model_2012 = models.IntegerField()
    model_2011 = models.IntegerField()
    model_2010 = models.IntegerField()

    def __str__(self):
        return f"{self.marka_adi} {self.tip_adi}"

    class Meta:
        verbose_name_plural = 'Araçlar'
"""
class PoliceTeklif(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    police_no = models.ForeignKey('Police', on_delete=models.CASCADE)
    brans_kodu = models.CharField(max_length=3)
    
    # Kasko ile ilgili alanlar
    plaka_il_kodu = models.IntegerField(blank=True, null=True)
    plaka_kodu = models.CharField(max_length=10, blank=True, null=True)
    arac_marka = models.CharField(max_length=255, blank=True, null=True)
    arac_model = models.CharField(max_length=255, blank=True, null=True)
    arac_model_yili = models.IntegerField(blank=True, null=True)
    motor_no = models.CharField(max_length=50, blank=True, null=True)
    sasi_no = models.CharField(max_length=50, blank=True, null=True)
    kasko_degeri = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    teklif_fiyati = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Sağlık sigortası ile ilgili alanlar
    yatarak_tedavi = models.BooleanField(default=False)
    ayakta_tedavi = models.BooleanField(default=False)
    asistans_paketi = models.BooleanField(default=False)
    doktor_danismanlik_hizmetleri = models.BooleanField(default=False)
    
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Teklifler'

    def __str__(self):
        return f"Teklif - Poliçe No: {self.police_no.police_no}"
"""

class SaglikBilgileri(models.Model):
    police_no = models.ForeignKey(Police, on_delete=models.CASCADE)
    yatarak_tedavi = models.BooleanField(default=False)
    ayakta_tedavi = models.BooleanField(default=False)
    asistans_paketi = models.BooleanField(default=False)
    doktor_danismanlik_hizmetleri = models.BooleanField(default=False)
    teklif_fiyati = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sağlık Bilgileri - Poliçe No: {self.police_no.police_no}"
    class Meta:
        verbose_name_plural = 'Saglik Poliçesi Bilgileri'

class SaglikPlanlar(models.Model):
    plan_adi = models.CharField(max_length=255)
    yatarak_tedavi = models.BooleanField(default=False)
    ayakta_tedavi = models.BooleanField(default=False)
    asistans_paketi = models.BooleanField(default=False)
    doktor_danismanlik_hizmetleri = models.BooleanField(default=False)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.plan_adi
    class Meta:
        verbose_name_plural = 'Saglik Planları'


from django.db import models
from django.conf import settings

class DaskBilgileri(models.Model):
    BINA_TIPI_CHOICES = [
        ('betonarme', 'Betonarme'),
        ('celik', 'Çelik'),
        ('ahsap', 'Ahşap'),
        ('yigma', 'Yığma'),
    ]

    RISK_BOLGESI_CHOICES = [
        ('bolge_1', 'Bölge 1 (En yüksek risk)'),
        ('bolge_2', 'Bölge 2'),
        ('bolge_3', 'Bölge 3'),
        ('bolge_4', 'Bölge 4'),
        ('bolge_5', 'Bölge 5 (En düşük risk)'),
    ]

    police_no = models.OneToOneField('Police', on_delete=models.CASCADE)
    bina_tipi = models.CharField(max_length=50, choices=BINA_TIPI_CHOICES)
    bina_yasi = models.IntegerField()
    kat_sayisi = models.IntegerField()
    bina_alani = models.FloatField()  # metrekare olarak
    risk_bolgesi = models.CharField(max_length=50, choices=RISK_BOLGESI_CHOICES)
    teklif_fiyati = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Dask Poliçeleri'

    def __str__(self):
        return f"DASK - {self.police_no.police_no}"
#