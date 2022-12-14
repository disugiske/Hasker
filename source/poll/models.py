import math
from django.db import models
from django.utils import timezone

from hasker import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def count(self):
        return f"{self.comments.count()}"

    def timeago(self):
        now = timezone.now()
        delta = now - self.date_posted
        seconds = delta.seconds
        minutes = math.floor(seconds / 60)
        hours = math.floor(seconds / 3600)
        days = delta.days
        months = math.floor(delta.days / 30)
        years = math.floor(delta.days / 365)
        if days == 0 and 0 <= seconds < 60:
            return f"{seconds} second ago"
        if days == 0 and 0 < minutes < 60:
            return f"{minutes} minutes ago"
        if days == 0 and hours > 0:
            return f"{hours} hours ago"
        if days > 0:
            return f"{days} days ago"
        if months > 0:
            return f"{months} months ago"
        if years > 0:
            return f"{years} years ago"


class PostTags(models.Model):
    post_tag = models.CharField(max_length=50)
    post_id = models.ForeignKey(Post, related_name="tags", on_delete=models.CASCADE)


class PostComments(models.Model):
    comment = models.TextField()
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    best = models.BooleanField(default=0)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        if len(self.comment) > 70:
            return f"{self.comment[:70]}..."
        return f"{self.comment}"


class VoteCommentCount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComments, on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)


class VotePostCount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_count = models.IntegerField(default=0)
