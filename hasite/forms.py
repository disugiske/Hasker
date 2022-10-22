from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from hasite.models import PostComments, Post


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AddPost(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "tags"]

    def clean(self):
        data = self.cleaned_data['tags']
        if len(data.split(",")) > 3:
            raise ValidationError("No more than 3 tags")
        return data


class AddCommentForm(ModelForm):
    class Meta:
        model = PostComments
        fields = ['comment']
