from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from api.serializers import (
    IndexSerializer,
    TendingSerializer,
    PostSerializer,
    CommentsSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
    TokenBlacklistResponseSerializer,
)
from hasite.models import Post, PostComments


class IndexViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.prefetch_related("tags", "comments", "author")
        .order_by("-date_posted")
        .select_related()
    )
    serializer_class = IndexSerializer
    http_method_names = ["get"]


class IndexHotViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.prefetch_related("tags", "comments", "author")
        .order_by("-votes", "-date_posted")
        .select_related()
    )
    serializer_class = IndexSerializer
    http_method_names = ["get"]


class TrendViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("tags", "comments", "author").order_by(
        "-votes", "-date_posted"
    )[:20]
    serializer_class = TendingSerializer
    paginator = None
    http_method_names = ["get"]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer
    http_method_names = ["get"]


class CommentView(viewsets.ModelViewSet):
    queryset = PostComments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["-rating", "-best"]
    paginator = None
    http_method_names = ["get"]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return PostComments.objects.filter(post=post_id).select_related()


class SearchView(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related(
        "tags", "comments", "author"
    ).select_related()
    serializer_class = IndexSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["-date_posted"]
    http_method_names = ["get"]

    def get_queryset(self):
        search = self.request.GET.get("word", "")
        tag = self.request.GET.get("tag", "")
        search_result = Post.objects.prefetch_related(
            "tags", "comments", "author"
        ).select_related()
        if tag:
            post = search_result.filter(Q(tags__post_tag__icontains=tag))
        elif search:
            post = search_result.filter(
                Q(title__icontains=search) | Q(text__icontains=search)
            )
        else:
            return Post.objects.none()
        return post


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
