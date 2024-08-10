from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Vehicle, Police, AracBilgileri, OdemeBilgileri, SaglikBilgileri, SaglikPlanlar, DaskBilgileri
import random
from django.http import JsonResponse
from .forms import DaskForm

# Kasko Detayı
def kasko_detail(request):
    markalar = Vehicle.objects.values_list('marka_adi', flat=True).distinct()
    model_yillari = [i for i in range(2024, 2009, -1)]
    return render(request, 'services/kasko_detail.html', {'markalar': markalar, 'model_yillari': model_yillari})

# Modelleri Getir
def get_models(request):
    marka = request.GET.get('marka')
    yil = request.GET.get('yil')
    modeller = Vehicle.objects.filter(marka_adi=marka).exclude(**{f'model_{yil}': 0}).values_list('tip_adi', flat=True).distinct()
    modeller_listesi = list(modeller)
    return JsonResponse(modeller_listesi, safe=False)

# Kasko Teklifi Al
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
            teklif_fiyati = kasko_degeri * 0.01 if kasko_degeri > 0 else "N/A"
        except Vehicle.DoesNotExist:
            kasko_degeri = "Değer bulunamadı"
            teklif_fiyati = "N/A"

        # Benzersiz bir police_no oluştur
        police_no = random.randint(10000000, 99999999)
        while Police.objects.filter(police_no=police_no).exists():
            police_no = random.randint(10000000, 99999999)

        # Poliçe ve Araç Bilgileri oluştur
        police = Police.objects.create(
            police_no=police_no,
            musteri_no=request.user,
            status='T',
            brans_kodu='340',  # Kasko branş kodu
            prim=teklif_fiyati,
            onaylayan=request.user,
            tanzim_tarihi=timezone.now(),
            baslangic_tarihi=timezone.now(),
            bitis_tarihi=timezone.now() + timezone.timedelta(days=15)
        )

        AracBilgileri.objects.create(
            police_no=police,
            plaka_il_kodu=plaka_il_kodu,
            plaka_kodu=plaka_kodu,
            arac_marka=arac_marka,
            arac_model=arac_model,
            arac_model_yili=arac_model_yili,
            teklif_fiyati=teklif_fiyati,
            motor_no='',  # Motor no eklenebilir
            sasi_no=''  # Şasi no eklenebilir
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

# Ödeme İşlemi
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
                cvv=cvv,
                odeme_tarihi=timezone.now(),
            )

            # Poliçe statusunu güncelle
            police.status = 'P'
            if police.brans_kodu == '610':  # Sağlık branş kodu
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=365)  # 1 yıllık poliçe
            elif police.brans_kodu == '340':  # Kasko branş kodu
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=15)  # 15 günlük poliçe
            elif police.brans_kodu == '199':  # DASK branş kodu
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=365)  # 1 yıllık poliçe
            police.save()

            return redirect('payment_success', police_id=police.id)
        else:
            return render(request, 'services/payment.html', {'police': police, 'error': 'Lütfen tüm alanları doldurun.'})

    return render(request, 'services/payment.html', {'police': police})



# Ödeme Başarılı
def payment_success(request, police_id):
    police = Police.objects.get(id=police_id)
    
    if police.brans_kodu == '610':  # Sağlık branş kodu
        saglik_bilgileri = SaglikBilgileri.objects.get(police_no=police)
        odeme_bilgileri = OdemeBilgileri.objects.get(police_no=police)
        saglik_bilgileri_formatted = {
            'yatarak_tedavi': 'Evet' if saglik_bilgileri.yatarak_tedavi else 'Hayır',
            'ayakta_tedavi': 'Evet' if saglik_bilgileri.ayakta_tedavi else 'Hayır',
            'asistans_paketi': 'Evet' if saglik_bilgileri.asistans_paketi else 'Hayır',
            'doktor_danismanlik_hizmetleri': 'Evet' if saglik_bilgileri.doktor_danismanlik_hizmetleri else 'Hayır'
        }
        
        return render(request, 'services/payment_success.html', {
            'police': police,
            'saglik_bilgileri': saglik_bilgileri_formatted,
            'odeme_bilgileri': odeme_bilgileri
        })
    elif police.brans_kodu == '340':  # Kasko branş kodu
        arac_bilgileri = AracBilgileri.objects.get(police_no=police)
        odeme_bilgileri = OdemeBilgileri.objects.get(police_no=police)
        return render(request, 'services/payment_success.html', {
            'police': police,
            'arac_bilgileri': arac_bilgileri,
            'odeme_bilgileri': odeme_bilgileri
        })
    elif police.brans_kodu == '199':  # DASK branş kodu
        dask_bilgileri = DaskBilgileri.objects.get(police_no=police)
        odeme_bilgileri = OdemeBilgileri.objects.get(police_no=police)
        
        return render(request, 'services/payment_success.html', {
            'police': police,
            'dask_bilgileri': dask_bilgileri,
            'odeme_bilgileri': odeme_bilgileri
        })
    else:
        return render(request, 'services/payment_success.html', {
            'police': police
        })

# Sağlık Sigorta Planlarını Listele
def health_insurance(request):
    saglik_planlari = SaglikPlanlar.objects.all()
    return render(request, 'services/health_insurance.html', {'saglik_planlari': saglik_planlari})

# Sağlık Teklifi Al (POST ile geliyor)
def get_health_offer(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        prim = request.POST.get('prim')

        # Benzersiz bir police_no oluştur
        police_no = random.randint(10000000, 99999999)
        while Police.objects.filter(police_no=police_no).exists():
            police_no = random.randint(10000000, 99999999)

        # Sağlık poliçesi oluştur
        police = Police.objects.create(
            police_no=police_no,
            musteri_no=request.user,
            status='T',
            brans_kodu='610',  # Sağlık branş kodu
            prim=prim,
            onaylayan=request.user,
            tanzim_tarihi=timezone.now(),
            baslangic_tarihi=timezone.now(),
            bitis_tarihi=timezone.now() + timezone.timedelta(days=365)  # 1 yıllık poliçe
        )

        # SaglikBilgileri kaydını oluştur
        SaglikBilgileri.objects.create(
            police_no=police,
            yatarak_tedavi=True if plan == "yatarak" else False,
            ayakta_tedavi=True if plan == "yatarak_ayakta" else False,
            asistans_paketi=True,
            doktor_danismanlik_hizmetleri=True,
            teklif_fiyati=prim,
        )

        return redirect('payment', police_id=police.id)

# Sağlık Planı Seçildiğinde İşlem Yap
def plan_select(request, plan_id):
    plan = get_object_or_404(SaglikPlanlar, id=plan_id)

    # Benzersiz bir police_no oluştur
    police_no = random.randint(10000000, 99999999)
    while Police.objects.filter(police_no=police_no).exists():
        police_no = random.randint(10000000, 99999999)

    # Sağlık poliçesi oluştur
    police = Police.objects.create(
        police_no=police_no,
        musteri_no=request.user,
        status='T',
        brans_kodu='610',  # Sağlık sigortası branş kodu
        prim=plan.fiyat,
        onaylayan=request.user,
        tanzim_tarihi=timezone.now(),
        baslangic_tarihi=timezone.now(),
        bitis_tarihi=timezone.now() + timezone.timedelta(days=365)  # 1 yıllık poliçe
    )

    # Sağlık bilgilerini oluştur
    SaglikBilgileri.objects.create(
        police_no=police,
        yatarak_tedavi=plan.yatarak_tedavi,
        ayakta_tedavi=plan.ayakta_tedavi,
        asistans_paketi=plan.asistans_paketi,
        doktor_danismanlik_hizmetleri=plan.doktor_danismanlik_hizmetleri,
        teklif_fiyati=plan.fiyat  # Teklif fiyatını burada kaydedin
    )

    # Kullanıcıyı ödeme sayfasına yönlendir
    return redirect('payment', police_id=police.id)

def dask_detail(request):
    if request.method == 'POST':
        form = DaskForm(request.POST)
        if form.is_valid():
            # Benzersiz bir police_no oluştur
            police_no = random.randint(10000000, 99999999)
            while Police.objects.filter(police_no=police_no).exists():
                police_no = random.randint(10000000, 99999999)

            # DASK poliçesi oluştur
            police = Police.objects.create(
                police_no=police_no,
                musteri_no=request.user,
                status='T',  # Başlangıçta Teklif statüsünde
                brans_kodu='199',  # DASK branş kodu
                prim=0,  # Başlangıçta prim 0 olarak kaydedilecek, teklif hesaplanacak
                onaylayan=request.user,
                tanzim_tarihi=timezone.now(),
                baslangic_tarihi=timezone.now(),
                bitis_tarihi=timezone.now() + timezone.timedelta(days=365)  # 1 yıllık poliçe
            )

            # Formu kaydet, police_no'yu ilişkilendir
            dask_bilgileri = form.save(commit=False)
            dask_bilgileri.police_no = police

            # Fiyatlandırma işlemi
            fiyat = hesapla_dask_fiyati(dask_bilgileri)
            dask_bilgileri.teklif_fiyati = fiyat
            dask_bilgileri.save()

            # Poliçe primini güncelle
            police.prim = fiyat
            police.save()

            # Ödeme sayfasına yönlendir
            return redirect('payment', police_id=police.id)

        else:
            return render(request, 'services/dask_detail.html', {'form': form, 'error': 'Form geçerli değil', 'form_errors': form.errors})
    else:
        form = DaskForm()

    return render(request, 'services/dask_detail.html', {'form': form})

def hesapla_dask_fiyati(dask_bilgileri):
    # Fiyat hesaplama işlemi
    fiyat = (
        dask_bilgileri.bina_alani * 10 +
        dask_bilgileri.kat_sayisi * 50 +
        dask_bilgileri.bina_yasi * 20 +
        (1 if dask_bilgileri.risk_bolgesi == '1' else 0.9) * 1000
    )
    return fiyat
