from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from hasker import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Hasker API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("poll.urls")),
    path("user/", include("users.urls")),
    path("api/v1/", include("api.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]


if settings.DEBUG:
    urlpatterns += (
        [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
        + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
