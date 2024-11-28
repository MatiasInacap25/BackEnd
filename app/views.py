from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  LoginForm, RegisterForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)  # Cambio aquí
        if form.is_valid():
            email = form.cleaned_data.get('username')  # El campo se llama username aunque sea email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
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
