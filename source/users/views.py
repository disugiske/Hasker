import asyncio

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tasks.sender import send_email
from poll.views import subject
from users.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        user_image = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid() and user_image.is_valid():
            form.save()
            user_image.save(commit=False)
            user_image.instance.user = form.instance
            user_image.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            messages.success(request, f"Создан аккаунт {username}!")
            message = (
                f"Hi {username},"
                f" you you been registered on hasker, login: https://hasker.site/auth/"
            )
            asyncio.run(
                send_email(
                    message=message, subject=subject["registration"], email=email
                )
            )
            return redirect("poll:index")
    else:
        form = UserRegisterForm()
        user_image = ProfileUpdateForm()
    return render(
        request, "user/registration.html", {"form": form, "user_image": user_image}
    )

@login_required
def account(request):
    if request.method == "POST":
        update_user = UserUpdateForm(request.POST, instance=request.user)
        update_profile = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user
        )
        if update_profile.is_valid():
            update_profile.save()
            messages.success(request, f"Ваше фото успешно обновлено")
        if update_user.is_valid():
            update_user.save()
            messages.success(request, f"Ваш профиль успешно обновлен")
        return redirect("users:account")

    else:
        update_user = UserUpdateForm(instance=request.user)
        update_profile = ProfileUpdateForm()
    return render(
        request,
        "user/account.html",
        {"update_user": update_user, "update_profile": update_profile},
    )
