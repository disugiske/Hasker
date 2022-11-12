from django.contrib.auth import views
from django.urls import path
from users.views import register, account

app_name = "users"

urlpatterns = [
    path("registration/", register, name="register"),
    path("auth/", views.LoginView.as_view(template_name="user/auth.html"), name="auth"),
    path("account/", account, name="account"),
    path(
            "logout/",
            views.LogoutView.as_view(template_name="user/logout.html"),
            name="logout",
        ),
    path(
            "account/reset_pass/",
            views.PasswordChangeView.as_view(
                template_name="user/reset_pass.html", success_url="users:account"
            ),
            name="change_password",
        ),
]