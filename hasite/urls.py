from django.conf import settings
from django.contrib.auth import views
from django.template.defaulttags import url
from django.urls import path, include
from django.conf.urls.static import static
from hasite.views import index, auth, register

app_name = "hasker"


urlpatterns = [
    path("", index, name="index"),
    path("registration", register, name="register"),
    path('auth/', views.LoginView.as_view(template_name='auth.html'), name='auth'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
