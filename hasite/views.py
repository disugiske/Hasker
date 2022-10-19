from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from hasite.forms import UserRegisterForm

@login_required(login_url="hasker:auth")
def index(request: HttpRequest):
    if request.method == 'GET':
        return render(request, "index.html")


def auth(request: HttpRequest):
    if request.user.username != "":
        return redirect('hasker:index')
    if request.method == 'POST':
        return render(request, "auth.html")


def register(request):
    if request.user.username != "":
        return redirect('hasker:index')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('hasker:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'auth.html')