from poll.models import Post, PostComments
from rest_framework import serializers


class IndexSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(source="comments.count")
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Post
        fields = ["title", "author", "votes", "comments", "timeago"]


class TendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "votes"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "title", "text", "author", "votes"]


class CommentsSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source="comment_author.username")
    post = serializers.CharField(source="post.title")

    class Meta:
        model = PostComments
        fields = ["post", "comment", "comment_author", "rating", "best"]


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
