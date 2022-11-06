from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from api.views import (
    IndexViewSet,
    IndexHotViewSet,
    TrendViewSet,
    PostViewSet,
    CommentView,
    SearchView,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"index", IndexViewSet, basename="index")
router.register(r"indexhot", IndexHotViewSet, basename="indexhot")
router.register(r"trending", TrendViewSet, basename="trending")
router.register(r"post", PostViewSet, basename="post")
router.register(r"post/(?P<post_id>\d*)/comments", CommentView)
router.register(r"search", SearchView, basename="search")

urlpatterns = [
    path("", include(router.urls)),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
