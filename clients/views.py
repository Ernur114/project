from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email уже зарегистрирован.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('task_list')

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, "Неверный логин или пароль.")

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
