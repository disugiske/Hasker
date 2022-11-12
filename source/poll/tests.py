import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from poll.forms import AddPost, Tags
from poll.models import Post, PostComments
from users.forms import UserRegisterForm, ProfileUpdateForm


class TestPages(TestCase):
    fixtures = ["user.json"]

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse("hasker:index"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("hasker:index_hot"))
        self.assertEqual(response.status_code, 200)

    def test_auth_req(self):
        response = self.client.get(reverse("hasker:account"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("hasker:change_password"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(path="/profile/NyanCat")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(path="/post/1")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("hasker:addpost"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/auth/?next=/addpost/")
        response = self.client.post(reverse("hasker:search"))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(path="/vote")
        self.assertEqual(response.status_code, 302)
        response = self.client.post(path="/best")
        self.assertEqual(response.status_code, 301)

    def test_auth_register(self):
        response = self.client.get(reverse("hasker:auth"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("hasker:register"))
        self.assertEqual(response.status_code, 200)


class TestFormsVote(TestCase):
    fixtures = ["user.json", "post.json", "comments.json", "profile.json"]

    def setUp(self):
        data = {"username": "testuser", "password": "123456789iI"}
        self.client = Client()
        self.client.post(path="/auth/", data=data)
        self.user = User.objects.get(username=data["username"])

    def test_page(self):
        data = ["hasker:addpost", "hasker:account", "hasker:change_password"]
        for i in data:
            response = self.client.get(reverse(i))
            self.assertEqual(response.status_code, 200, msg=f"error in {i}")
        response = self.client.get(path="/profile/testuser")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(path="/post/1")
        self.assertEqual(response.status_code, 200)

    def test_addpost(self):
        data = {"title": "whats up?", "text": "Lorem ipsum"}
        form = AddPost(data=data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            post = Post.objects.create(
                author=self.user, title=data["title"], text=data["text"]
            )
            response = self.client.get(f"/post/{post.id}")
            self.assertEqual(response.status_code, 200)

    def test_tags(self):
        data = {"post_tag": "hello, name, test, what"}
        data_true = {"post_tag": "hello, name, test"}
        form = Tags(data=data)
        self.assertFalse(form.is_valid())
        form = Tags(data=data_true)
        self.assertTrue(form.is_valid())

    def test_add_comment(self):
        data = {"title": "whats up?", "text": "Lorem ipsum"}
        post = Post.objects.create(
            author=self.user, title=data["title"], text=data["text"]
        )
        response = self.client.post(
            path=f"/post/{post.id}",
            data={"comment": "hello world", "comment_author": self.user},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/post/{post.id}")

    def test_vote_comment(self):
        data = {"up": 1, "vote_id": 1, "method": "comment_vote"}
        data_down = {"down": 1, "vote_id": 1, "method": "comment_vote"}
        rating_start = PostComments.objects.get(id=data["vote_id"]).rating
        response = self.client.post(path="/vote", data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start + 1, msg="err vote up")

        response = self.client.post(path="/vote", data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote up double")

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg="err vote down")

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(
            rating, rating_start - 1, msg="err vote down double after plus"
        )

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote down double")

    def test_vote_post(self):
        data = {"up": 1, "vote_id": 1, "method": "post_vote"}
        data_down = {"down": 1, "vote_id": 1, "method": "post_vote"}
        rating_start = Post.objects.get(id=data["vote_id"]).votes
        response = self.client.post(path="/vote", data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start + 1, msg="err vote up")

        response = self.client.post(path="/vote", data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote up double")

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg="err vote down")

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(
            rating, rating_start - 1, msg="err vote down double after plus"
        )

        response = self.client.post(path="/vote", data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote down double")

    def test_best_comment(self):
        data = {"comment_id": 14}
        response = self.client.post(path="/best/", data=data)

        bests = PostComments.objects.get(id=data["comment_id"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bests.best)

        data_new = {"comment_id": 13}
        response = self.client.post(path="/best/", data=data_new)
        bests = PostComments.objects.get(id=data_new["comment_id"]).best
        ex_best = PostComments.objects.get(id=data["comment_id"]).best
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bests)
        self.assertFalse(ex_best)

    # def test_forbidden_best(self):
    #     data = {"comment_id": 1}
    #     response = self.client.post(path="/best/", data=data)
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_register(self):
    #     data = {
    #         "username": "test",
    #         "email": "test@test.com",
    #         "password1": "supersecret22",
    #         "password2": "supersecret22",
    #     }
    #     form = UserRegisterForm(data)
    #     self.assertTrue(form.is_valid())
    #     if form.is_valid():
    #         form.save()
    #     user = User.objects.filter(username="test")
    #     self.assertTrue(user)
    #
    # def test_search(self):
    #     data = {"search": "Lorem ipsum"}
    #     response = self.client.post(path="/search/", data=data)
    #     self.assertEqual(response.status_code, 200)
    #     request = response._container[0].decode()
    #     self.assertTrue("Where can I get some?" in request)
    #
    # def test_search_tags(self):
    #     data = {"tag": "django"}
    #     response = self.client.post(path="/search/", data=data)
    #     self.assertTrue("How are you doing?" in response._container[0].decode())
    #
    # def test_update_profile(self):
    #     image = SimpleUploadedFile(
    #         name="test.jpg", content=b"", content_type="image/jpeg"
    #     )
    #     form = ProfileUpdateForm(image)
    #     self.assertTrue(form.is_valid())
