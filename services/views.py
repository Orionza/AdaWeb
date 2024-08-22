from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Vehicle, Police, AracBilgileri, OdemeBilgileri, SaglikBilgileri, SaglikPlanlar, DaskBilgileri
import random
from django.http import JsonResponse
from .forms import DaskForm, AracBilgileriForm, PaymentForm
from django.contrib.auth.decorators import login_required
import re


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
        # Form verilerini alın
        plaka_il_kodu = request.POST.get('plaka_il_kodu')
        plaka_kodu = request.POST.get('plaka_kodu')
        arac_marka = request.POST.get('arac_marka')
        arac_model_yili = request.POST.get('arac_model_yili')
        arac_model = request.POST.get('arac_model')
        motor_no = request.POST.get('motor_no')
        sasi_no = request.POST.get('sasi_no')

        
        error_messages = []

        
        if not plaka_il_kodu or not plaka_il_kodu.isdigit() or not (10 <= int(plaka_il_kodu) <= 99):
            error_messages.append("Plaka il kodu 2 basamaklı bir sayı olmalıdır.")

        
        if not plaka_kodu or len(plaka_kodu) > 7 or not any(char.isdigit() for char in plaka_kodu) or not any(char.isalpha() for char in plaka_kodu):
            error_messages.append("Plaka kodu maksimum 7 karakter uzunluğunda olmalı ve en az bir harf ile en az bir rakam içermelidir.")

        
        if not motor_no or len(motor_no) != 15 or not motor_no.isalnum():
            error_messages.append("Motor numarası 15 karakter uzunluğunda olmalı ve sadece harf ve rakam içermelidir.")

        
        if not sasi_no or len(sasi_no) != 17 or not sasi_no.isalnum():
            error_messages.append("Şasi numarası 17 karakter uzunluğunda olmalı ve sadece harf ve rakam içermelidir.")

        
        if error_messages:
            return render(request, 'services/kasko_detail.html', {
                'markalar': Vehicle.objects.values_list('marka_adi', flat=True).distinct(),
                'model_yillari': [i for i in range(2024, 2009, -1)],
                'plaka_il_kodu': plaka_il_kodu,
                'plaka_kodu': plaka_kodu,
                'arac_marka': arac_marka,
                'arac_model_yili': arac_model_yili,
                'arac_model': arac_model,
                'motor_no': motor_no,
                'sasi_no': sasi_no,
                'error_messages': error_messages,
            })

        try:
            vehicle = Vehicle.objects.get(marka_adi=arac_marka, tip_adi=arac_model)
            kasko_degeri = getattr(vehicle, f'model_{arac_model_yili}', 0)
            teklif_fiyati = kasko_degeri * 0.01346 if kasko_degeri > 0 else None
        except Vehicle.DoesNotExist:
            kasko_degeri = None
            teklif_fiyati = None

        
        if teklif_fiyati is None:
            teklif_fiyati = 0

        
        police_no = random.randint(10000000, 99999999)
        while Police.objects.filter(police_no=police_no).exists():
            police_no = random.randint(10000000, 99999999)

        # Poliçe ve Araç Bilgileri oluştur
        police = Police.objects.create(
            police_no=police_no,
            musteri_no=request.user,
            status='T',
            brans_kodu='340',
            prim=teklif_fiyati,
            onaylayan=request.user,
            tanzim_tarihi=timezone.now(),
            baslangic_tarihi=timezone.now(),
            bitis_tarihi=timezone.now() + timezone.timedelta(days=15)
        )

        AracBilgileri.objects.create(
            police_no=police,
            plaka_il_kodu=int(plaka_il_kodu),
            plaka_kodu=plaka_kodu,
            arac_marka=arac_marka,
            arac_model=arac_model,
            arac_model_yili=int(arac_model_yili),
            motor_no=motor_no,
            sasi_no=sasi_no,
            teklif_fiyati=teklif_fiyati
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
            'motor_no': motor_no,
            'sasi_no': sasi_no,
            'arac_modeller': Vehicle.objects.filter(marka_adi=arac_marka).exclude(**{f'model_{arac_model_yili}': 0}).values_list('tip_adi', flat=True).distinct(),
            'show_payment_button': True,
            'police_id': police.id
        })

    return render(request, 'services/kasko_detail.html', {
        'markalar': Vehicle.objects.values_list('marka_adi', flat=True).distinct(),
        'model_yillari': [i for i in range(2024, 2009, -1)]
    })



# Ödeme İşlemi
@login_required
def payment(request, police_id):
    police = Police.objects.get(id=police_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            
            kredi_kart_no = form.cleaned_data['kredi_kart_no']
            kredi_kart_sahibi = form.cleaned_data['kredi_kart_sahibi']
            son_kullanma_tarihi = form.cleaned_data['son_kullanma_tarihi']
            cvv = form.cleaned_data['cvv']
            odeme_tutari = police.prim

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

            # Poliçe başlangıç tarihini ödeme tarihi olarak değiştirdim
            police.baslangic_tarihi = timezone.now()
            police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=365)
            police.status = 'P'
            police.save()

            return redirect('payment_success', police_id=police.id)
    else:
        form = PaymentForm()

    return render(request, 'services/payment.html', {'police': police, 'form': form})







# Ödeme Başarılı
def payment_success(request, police_id):
    try:
        police = Police.objects.get(id=police_id)
    except Police.DoesNotExist:
        return render(request, 'services/payment_error.html', {'error': 'Poliçe bulunamadı.'})

    odeme_bilgileri = None
    saglik_bilgileri_formatted = None
    arac_bilgileri = None
    dask_bilgileri = None

    try:
        odeme_bilgileri = OdemeBilgileri.objects.get(police_no=police)
    except OdemeBilgileri.DoesNotExist:
        return render(request, 'services/payment_error.html', {'error': 'Ödeme bilgileri bulunamadı.'})

    if police.brans_kodu == '610':  # Sağlık sigortası
        try:
            saglik_bilgileri = SaglikBilgileri.objects.get(police_no=police)
            saglik_bilgileri_formatted = {
                'yatarak_tedavi': 'Evet' if saglik_bilgileri.yatarak_tedavi else 'Hayır',
                'ayakta_tedavi': 'Evet' if saglik_bilgileri.ayakta_tedavi else 'Hayır',
                'asistans_paketi': 'Evet' if saglik_bilgileri.asistans_paketi else 'Hayır',
                'doktor_danismanlik_hizmetleri': 'Evet' if saglik_bilgileri.doktor_danismanlik_hizmetleri else 'Hayır'
            }
        except SaglikBilgileri.DoesNotExist:
            return render(request, 'services/payment_error.html', {'error': 'Sağlık bilgileri bulunamadı.'})
        
        return render(request, 'services/payment_success.html', {
            'police': police,
            'saglik_bilgileri': saglik_bilgileri_formatted,
            'odeme_bilgileri': odeme_bilgileri
        })

    elif police.brans_kodu == '340':  # Kasko sigortası
        try:
            arac_bilgileri = AracBilgileri.objects.get(police_no=police)
        except AracBilgileri.DoesNotExist:
            return render(request, 'services/payment_error.html', {'error': 'Araç bilgileri bulunamadı.'})
        
        return render(request, 'services/payment_success.html', {
            'police': police,
            'arac_bilgileri': arac_bilgileri,
            'odeme_bilgileri': odeme_bilgileri
        })

    elif police.brans_kodu == '199':  # DASK sigortası
        try:
            dask_bilgileri = DaskBilgileri.objects.get(police_no=police)
        except DaskBilgileri.DoesNotExist:
            return render(request, 'services/payment_error.html', {'error': 'DASK bilgileri bulunamadı.'})
        
        return render(request, 'services/payment_success.html', {
            'police': police,
            'dask_bilgileri': dask_bilgileri,
            'odeme_bilgileri': odeme_bilgileri
        })

    else:
        return render(request, 'services/payment_error.html', {'error': 'Geçersiz branş kodu.'})

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
        brans_kodu='610',  
        prim=plan.fiyat,
        onaylayan=request.user,
        tanzim_tarihi=timezone.now(),
        baslangic_tarihi=timezone.now(),
        bitis_tarihi=timezone.now() + timezone.timedelta(days=365)  
    )

    # Sağlık bilgilerini oluştur
    SaglikBilgileri.objects.create(
        police_no=police,
        yatarak_tedavi=plan.yatarak_tedavi,
        ayakta_tedavi=plan.ayakta_tedavi,
        asistans_paketi=plan.asistans_paketi,
        doktor_danismanlik_hizmetleri=plan.doktor_danismanlik_hizmetleri,
        teklif_fiyati=plan.fiyat  
    )

    # Kullanıcıyı ödeme sayfasına yönlendir
    return redirect('payment', police_id=police.id)

def dask_detail(request):
    if request.method == 'POST':
        form = DaskForm(request.POST)
        if 'teklif_al' in request.POST:  # Teklif Al butonuna basıldıysa
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
                    brans_kodu='199',  
                    prim=0,  # Başlangıçta prim 0 olarak kaydedilecek, teklif hesaplanacak
                    onaylayan=request.user,
                    tanzim_tarihi=timezone.now(),
                    baslangic_tarihi=timezone.now(),
                    bitis_tarihi=timezone.now() + timezone.timedelta(days=365)  
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

                # Poliçeleştir butonunu göster
                return render(request, 'services/dask_detail.html', {
                    'form': form,
                    'fiyat': fiyat,
                    'police_id': police.id,
                    'show_policelestir': True
                })

        elif 'policelestir' in request.POST:  # Poliçeleştir butonuna basıldıysa
            police_id = request.POST.get('police_id')
            return redirect('payment', police_id=police_id)

        else:
            return render(request, 'services/dask_detail.html', {'form': form, 'error': 'Form geçerli değil'})
    else:
        form = DaskForm()

    return render(request, 'services/dask_detail.html', {'form': form})



def hesapla_dask_fiyati(dask_bilgileri):
    # Fiyat hesaplama işlemim
    fiyat = (
        dask_bilgileri.bina_alani * 10 +
        dask_bilgileri.kat_sayisi * 50 +
        dask_bilgileri.bina_yasi * 20 +
        (1 if dask_bilgileri.risk_bolgesi == '1' else 0.9) * 1000
    )
    return fiyat
