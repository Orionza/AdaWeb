from django.db import models
from django.conf import settings
import random

class Police(models.Model):
    POLICE_STATUS_CHOICES = [
        ('T', 'Teklif'),
        ('P', 'Poliçeleşmiş')
    ]

    police_no = models.IntegerField(unique=True)
    musteri_no = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=POLICE_STATUS_CHOICES)
    brans_kodu = models.CharField(max_length=3)
    prim = models.DecimalField(max_digits=10, decimal_places=2)
    onaylayan = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='onaylayan', on_delete=models.CASCADE)
    tanzim_tarihi = models.DateTimeField(auto_now_add=True)
    baslangic_tarihi = models.DateTimeField()
    bitis_tarihi = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Poliçeler'

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
    plaka_kodu = models.CharField(max_length=10)
    arac_marka = models.CharField(max_length=255)
    arac_model = models.CharField(max_length=255)
    arac_model_yili = models.IntegerField()
    motor_no = models.CharField(max_length=50, blank=True)
    sasi_no = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Poliçe Araç Bilgileri'

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

class PoliceTeklif(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    police_no = models.ForeignKey(Police, on_delete=models.CASCADE)
    plaka_il_kodu = models.IntegerField()
    plaka_kodu = models.CharField(max_length=10)
    arac_marka = models.CharField(max_length=255)
    arac_model = models.CharField(max_length=255)
    arac_model_yili = models.IntegerField()
    motor_no = models.CharField(max_length=50, blank=True)
    sasi_no = models.CharField(max_length=50, blank=True)
    kasko_degeri = models.DecimalField(max_digits=10, decimal_places=2)
    teklif_fiyati = models.DecimalField(max_digits=10, decimal_places=2)
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Teklifler'
