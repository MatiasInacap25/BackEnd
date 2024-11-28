from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  LoginForm, RegisterForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, '¡Bienvenido!')
                return redirect('home')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
    return render(request, 'register.html', {'form': form})

@login_required()
def home(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    messages.success(request, '¡Hasta pronto!')
    return redirect('login')

