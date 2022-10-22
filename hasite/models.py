from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    tags = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # comments = models.ForeignKey('PostComments', on_delete=models.CASCADE, default=None)


class PostComments(models.Model):
    comment = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    best = models.BooleanField(default=0)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)


class VoteCommentCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComments, on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)


class VotePostCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_count = models.IntegerField(default=0)
