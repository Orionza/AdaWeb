from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse



def register(request):
    if request.method == 'POST':
        print(request.POST)  # Burada request.POST içeriğini kontrol edebilirsiniz
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
    return render(request, 'services.html')#buralar da dolacak

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')

def kasko_detail(request):
    return render(request, 'services/kasko_detail.html')
