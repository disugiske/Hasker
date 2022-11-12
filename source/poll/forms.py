from django.core.exceptions import ValidationError
from django.forms import ModelForm

from poll.models import PostComments, Post, PostTags


class Tags(ModelForm):
    class Meta:
        model = PostTags
        fields = ["post_tag"]

    def clean_post_tag(self):
        data = self.cleaned_data["post_tag"]
        if len(data.split(",")) > 3:
            raise ValidationError("No more than 3 tags")
        return data


class AddPost(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text"]


class AddCommentForm(ModelForm):
    class Meta:
        model = PostComments
        fields = ["comment"]
