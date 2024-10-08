from django.contrib import admin
from .models import Police, AracBilgileri, OdemeBilgileri, Vehicle, SaglikBilgileri, SaglikPlanlar, DaskBilgileri
from accounts.models import MyUser

@admin.register(Police)
class PoliceAdmin(admin.ModelAdmin):
    list_display = ('police_no', 'musteri_no', 'status', 'brans_kodu', 'prim', 'tanzim_tarihi', 'baslangic_tarihi', 'bitis_tarihi')
    list_filter = ('status', 'brans_kodu')
    search_fields = ('status','musteri_no__id')

@admin.register(AracBilgileri)
class AracBilgileriAdmin(admin.ModelAdmin):
    list_display = ('police_no', 'plaka_il_kodu', 'plaka_kodu', 'arac_marka', 'arac_model', 'arac_model_yili', 'motor_no', 'sasi_no')
    search_fields = ('police_no__police_no', 'plaka_kodu', 'arac_marka', 'arac_model')

@admin.register(OdemeBilgileri)
class OdemeBilgileriAdmin(admin.ModelAdmin):
    list_display = ('police_no', 'odeme_tutari', 'odeme_tarihi', 'kredi_kart_no', 'kredi_kart_sahibi', 'son_kullanma_tarihi', 'cvv')
    search_fields = ('police_no__police_no', 'kredi_kart_no', 'kredi_kart_sahibi')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('marka_kodu', 'tip_kodu', 'marka_adi', 'tip_adi', 'model_2024', 'model_2023', 'model_2022', 'model_2021', 'model_2020', 'model_2019', 'model_2018', 'model_2017', 'model_2016', 'model_2015', 'model_2014', 'model_2013', 'model_2012', 'model_2011', 'model_2010')
    list_filter = ('marka_adi',)
    search_fields = ('marka_adi', 'tip_adi', 'marka_kodu', 'tip_kodu')
"""
@admin.register(PoliceTeklif)
class PoliceTeklifAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_police_no', 'plaka_il_kodu', 'plaka_kodu', 'arac_marka', 'arac_model', 'arac_model_yili', 'motor_no', 'sasi_no', 'kasko_degeri', 'teklif_fiyati', 'tarih')
    search_fields = ('user__id', 'police_no__police_no', 'plaka_kodu', 'arac_marka', 'arac_model')

    def get_police_no(self, obj):
        return obj.police_no.police_no
    get_police_no.short_description = 'Police No'
"""
@admin.register(SaglikBilgileri)
class SaglikBilgileriAdmin(admin.ModelAdmin):
    list_display = ('police_no', 'yatarak_tedavi', 'ayakta_tedavi', 'asistans_paketi', 'doktor_danismanlik_hizmetleri')
    search_fields = ('police_no__police_no', 'yatarak_tedavi', 'ayakta_tedavi', 'asistans_paketi', 'doktor_danismanlik_hizmetleri')  # Poliçe numarası ile arama yapma imkanı

@admin.register(SaglikPlanlar)
class SaglikPlanlarAdmin(admin.ModelAdmin):
    list_display = ('plan_adi', 'yatarak_tedavi', 'ayakta_tedavi', 'asistans_paketi', 'doktor_danismanlik_hizmetleri', 'fiyat')
    search_fields = ('plan_adi',)

@admin.register(DaskBilgileri)
class DaskBilgileriAdmin(admin.ModelAdmin):
    list_display = ('police_no', 'bina_tipi', 'bina_yasi', 'kat_sayisi', 'bina_alani', 'risk_bolgesi', 'teklif_fiyati')
    search_fields = ('police_no__police_no', 'bina_tipi')
    list_filter = ('bina_tipi', 'risk_bolgesi')



# Alternatif olarak register yöntemiyle de modelleri ekleyebilirdim.:
# admin.site.register(Police, PoliceAdmin)
# admin.site.register(AracBilgileri, AracBilgileriAdmin)
# admin.site.register(OdemeBilgileri, OdemeBilgileriAdmin)
# admin.site.register(Vehicle, VehicleAdmin)


