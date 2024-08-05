from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Vehicle, Police, AracBilgileri, PoliceTeklif, OdemeBilgileri
import random

User = get_user_model()

def kasko_detail(request):
    markalar = Vehicle.objects.values_list('marka_adi', flat=True).distinct()
    model_yillari = [i for i in range(2024, 2009, -1)]
    return render(request, 'services/kasko_detail.html', {'markalar': markalar, 'model_yillari': model_yillari})

def get_models(request):
    marka = request.GET.get('marka')
    yil = request.GET.get('yil')
    modeller = Vehicle.objects.filter(marka_adi=marka).exclude(**{f'model_{yil}': 0}).values_list('tip_adi', flat=True).distinct()
    modeller_listesi = list(modeller)
    return JsonResponse(modeller_listesi, safe=False)

def get_offer(request):
    if request.method == 'POST':
        plaka_il_kodu = request.POST['plaka_il_kodu']
        plaka_kodu = request.POST['plaka_kodu']
        arac_marka = request.POST['arac_marka']
        arac_model_yili = request.POST['arac_model_yili']
        arac_model = request.POST['arac_model']

        try:
            vehicle = Vehicle.objects.get(marka_adi=arac_marka, tip_adi=arac_model)
            kasko_degeri = getattr(vehicle, f'model_{arac_model_yili}')

            if kasko_degeri > 0:
                teklif_fiyati = kasko_degeri * 0.01
            else:
                kasko_degeri = "Değer bulunamadı"
                teklif_fiyati = "N/A"
        except Vehicle.DoesNotExist:
            kasko_degeri = "Değer bulunamadı"
            teklif_fiyati = "N/A"

        # Benzersiz bir police_no oluştur
        police_no = random.randint(10000000, 99999999)
        while Police.objects.filter(police_no=police_no).exists():
            police_no = random.randint(10000000, 99999999)

        # Poliçe oluştur
        police = Police.objects.create(
            police_no=police_no,
            musteri_no=request.user,
            status='T',
            brans_kodu='340',  # Örnek branş kodu
            prim=teklif_fiyati,
            onaylayan=request.user,
            tanzim_tarihi=timezone.now(),
            baslangic_tarihi=timezone.now(),
            bitis_tarihi=timezone.now() + timezone.timedelta(days=15)
        )

        # Araç bilgilerini oluştur
        AracBilgileri.objects.create(
            police_no=police,
            plaka_il_kodu=plaka_il_kodu,
            plaka_kodu=plaka_kodu,
            arac_marka=arac_marka,
            arac_model=arac_model,
            arac_model_yili=arac_model_yili,
            motor_no='',  # Motor no eklenebilir
            sasi_no=''  # Şasi no eklenebilir
        )

        # Teklif bilgilerini oluştur
        PoliceTeklif.objects.create(
            user=request.user,
            police_no=police,
            plaka_il_kodu=plaka_il_kodu,
            plaka_kodu=plaka_kodu,
            arac_marka=arac_marka,
            arac_model=arac_model,
            arac_model_yili=arac_model_yili,
            kasko_degeri=kasko_degeri,
            teklif_fiyati=teklif_fiyati,
            motor_no='',
            sasi_no=''
        )

        return render(request, 'services/kasko_detail.html', {
            'markalar': Vehicle.objects.values_list('marka_adi', flat=True).distinct(),
            'model_yillari': [i for i in range(2024, 2009, -1)],
            'kasko_degeri': kasko_degeri,
            'teklif_fiyati': teklif_fiyati,
            'plaka_il_kodu': plaka_il_kodu,
            'plaka_kodu': plaka_kodu,
            'arac_marka': arac_marka,
            'arac_model_yili': arac_model_yili,
            'arac_model': arac_model,
            'arac_modeller': Vehicle.objects.filter(marka_adi=arac_marka).exclude(**{f'model_{arac_model_yili}': 0}).values_list('tip_adi', flat=True).distinct(),
            'show_payment_button': True,
            'police_id': police.id
        })

    return render(request, 'services/kasko_detail.html', {
        'markalar': Vehicle.objects.values_list('marka_adi', flat=True).distinct(),
        'model_yillari': [i for i in range(2024, 2009, -1)]
    })

def payment(request, police_id):
    police = Police.objects.get(id=police_id)
    if request.method == 'POST':
        kredi_kart_no = request.POST.get('kredi_kart_no')
        kredi_kart_sahibi = request.POST.get('kredi_kart_sahibi')
        son_kullanma_tarihi = request.POST.get('son_kullanma_tarihi')
        cvv = request.POST.get('cvv')
        odeme_tutari = police.prim

        if kredi_kart_no and kredi_kart_sahibi and son_kullanma_tarihi and cvv:
            # Ödeme bilgilerini kaydet
            OdemeBilgileri.objects.create(
                police_no=police,
                odeme_tutari=odeme_tutari,
                kredi_kart_no=kredi_kart_no,
                kredi_kart_sahibi=kredi_kart_sahibi,
                son_kullanma_tarihi=son_kullanma_tarihi,
                cvv=cvv
            )

            # Poliçe statusunu güncelle
            police.status = 'P'
            police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=15)
            police.save()

            return redirect('payment_success', police_id=police.id)
        else:
            # Eksik veri varsa bir hata mesajı dönebiliriz
            return render(request, 'services/payment.html', {'police': police, 'error': 'Lütfen tüm alanları doldurun.'})

    return render(request, 'services/payment.html', {'police': police})


def payment_success(request, police_id):
    police = Police.objects.get(id=police_id)
    arac_bilgileri = AracBilgileri.objects.get(police_no=police)
    odeme_bilgileri = OdemeBilgileri.objects.get(police_no=police)

    return render(request, 'services/payment_success.html', {
        'police': police,
        'arac_bilgileri': arac_bilgileri,
        'odeme_bilgileri': odeme_bilgileri
    })
