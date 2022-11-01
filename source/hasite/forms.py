from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from hasite.models import PostComments, Post, PostTags, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class Tags(ModelForm):
    class Meta:
        model = PostTags
        fields = ["post_tag"]

    def clean_post_tag(self):
        data = self.cleaned_data['post_tag']
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
        fields = ['comment']


class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)