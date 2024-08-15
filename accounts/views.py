from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from services.models import Police
from django.utils import timezone
from services.models import Vehicle, Police, AracBilgileri, OdemeBilgileri, SaglikBilgileri, SaglikPlanlar, DaskBilgileri



def register(request):
    if request.method == 'POST':
        print(request.POST)  
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesabınız başarıyla oluşturuldu. Artık giriş yapabilirsiniz.')
            return redirect('login')
        else:
            messages.error(request, 'Kayıt işlemi sırasında bir hata oluştu. Lütfen form alanlarını kontrol edin.')
            print(form.errors)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        id_number = request.POST['id_number']
        password = request.POST['password']
        user = authenticate(request, username=id_number, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Geçersiz giriş bilgileri.')
    return render(request, 'accounts/login.html')


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def logout_view(request):
    logout(request)
    return redirect('home') 


@login_required
def user_profile(request):
    user = request.user
    teklif_policeler = Police.objects.filter(musteri_no=user, status='T')
    policelenmis_policeler = Police.objects.filter(musteri_no=user, status='P')
    
    # Branş kodlarına karşılık gelen sigorta isimleri
    brans_isimleri = {
        '199': 'Dask',
        '340': 'Kasko',
        '610': 'Sağlık'
    }

    # Poliçelerin sigorta türü isimleri ile birlikte şablona gönderilmesi
    teklif_policeler = [
        {
            "id": police.id,  
            "police_no": police.police_no,
            "brans_adi": brans_isimleri.get(police.brans_kodu, police.brans_kodu),
            "prim": police.prim,
            "baslangic_tarihi": police.baslangic_tarihi,
            "bitis_tarihi": police.bitis_tarihi,
        } for police in teklif_policeler
    ]

    policelenmis_policeler = [
        {
            "id": police.id,  
            "police_no": police.police_no,
            "brans_adi": brans_isimleri.get(police.brans_kodu, police.brans_kodu),
            "prim": police.prim,
            "baslangic_tarihi": police.baslangic_tarihi,
            "bitis_tarihi": police.bitis_tarihi,
        } for police in policelenmis_policeler
    ]
    
    context = {
        'teklif_policeler': teklif_policeler,
        'policelemes_policeler': policelenmis_policeler,
    }
    
    return render(request, 'accounts/user_profile.html', context)


def kasko_detail(request):
    return render(request, 'services/kasko_detail.html')

@login_required
def odeme_yap(request, police_id):
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
            if police.brans_kodu == '610':  
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=365)  
            elif police.brans_kodu == '340':  
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=15)  
            elif police.brans_kodu == '199':  
                police.bitis_tarihi = police.baslangic_tarihi + timezone.timedelta(days=365)  
            police.save()

            return redirect('payment_success', police_id=police.id)
        else:
            return render(request, 'services/payment.html', {'police': police, 'error': 'Lütfen tüm alanları doldurun.'})

    return render(request, 'services/payment.html', {'police': police})

@login_required
def iptal_et(request, police_id):
    try:
        police = Police.objects.get(id=police_id, musteri_no=request.user)
        police.delete()  # Poliçeyi sil
        return redirect('user_profile')  # Profil sayfasına yönlendir
    except Police.DoesNotExist:
        # Eğer poliçe bulunamazsa bir hata mesajı gösterin
        messages.error(request, "Bu poliçe bulunamadı veya size ait değil.")
        return redirect('user_profile')  # Profil sayfasına yönlendir

