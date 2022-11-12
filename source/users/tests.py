from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.forms import ProfileUpdateForm, UserRegisterForm
from users.models import Profile


class TestPages(TestCase):
    fixtures = ["users.json"]

    def test_auth_register(self):
        response = self.client.get(reverse("users:auth"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth(self):
        data = {"username": 'admin',
                "password": '123456'}

        response = self.client.post("/user/auth/", data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_register(self):
        data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "supersecret22",
            "password2": "supersecret22",
        }
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save()
        user = Profile.objects.filter(username="test")
        self.assertTrue(user)

    def test_update_profile(self):
        image = SimpleUploadedFile(
            name="test.jpg", content=b"", content_type="image/jpeg"
        )
        form = ProfileUpdateForm(image)
        self.assertTrue(form.is_valid())
