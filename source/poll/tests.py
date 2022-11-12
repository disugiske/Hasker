import json

from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from hasker import settings
from poll.forms import AddPost, Tags
from poll.models import Post, PostComments
from users.models import Profile


class TestPages(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.customer = baker.make(settings.AUTH_USER_MODEL)

    def test_index(self):
        response = self.client.get(reverse("poll:index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("poll:index_hot"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auths_account(self):
        response = self.client.get(reverse("users:account"), follow=True)
        self.assertTrue(response.redirect_chain)

    def test_auths_changepass(self):
        response = self.client.get(reverse("users:change_password"), follow=True)
        self.assertTrue(response.redirect_chain)

    def test_auth_profile(self):
        response = self.client.get(path=f"/profile/{self.customer.username}", follow=True)
        self.assertTrue(response.redirect_chain)

    def test_auth_post(self):
        response = self.client.get(path=f"/post/1", follow=True)
        self.assertTrue(response.redirect_chain)

    def test_addpost(self):
        response = self.client.get(reverse("poll:addpost"), follow=True)
        self.assertTrue(response.redirect_chain)

    def test_search(self):
        response = self.client.post(reverse("poll:search"), follow=True)
        self.assertTrue(response.redirect_chain)

    def test_vote(self):
        response = self.client.post(reverse("poll:vote"), follow=True)
        self.assertTrue(response.redirect_chain)

    def test_best(self):
        response = self.client.post(reverse("poll:best_choice"), follow=True)
        self.assertTrue(response.redirect_chain)


class TestPagesPost(TestCase):
    fixtures = ['users.json', 'tags.json', 'posts.json', 'comment.json']

    def setUp(self):
        data = {"username": "testuser", "password": "123456789iI"}
        self.client = Client()

        self.user = Profile.objects.get(username=data["username"])
        self.client.force_login(self.user)

    def test_page(self):
        data = ["poll:addpost", "users:account", "users:change_password"]
        for i in data:
            response = self.client.get(reverse(i))
            self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"error in {i}")
        response = self.client.get(path=f"/profile/NyanCat")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(path="/post/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_addpost(self):
        data = {"title": "whats up?", "text": "Lorem ipsum"}
        form = AddPost(data=data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            post = Post.objects.create(
                author=self.user, title=data["title"], text=data["text"]
            )
            response = self.client.get(f"/post/{post.id}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)



class TestComments(TestCase):
    fixtures = ['users.json', 'tags.json', 'posts.json', 'comment.json']
    def setUp(self):
        data = {"username": "testuser", "password": "123456789iI"}
        self.client = Client()
        self.user = Profile.objects.get(username=data["username"])
        self.client.force_login(self.user)

    def test_add_comment(self):
        data = {"title": "whats up?", "text": "Lorem ipsum"}
        post = Post.objects.create(
            author=self.user, title=data["title"], text=data["text"]
        )
        response = self.client.post(
            path=f"/post/{post.id}",
            data={"comment": "hello world", "comment_author": self.user},
            follow=True
        )
        self.assertTrue(response.redirect_chain)

    def test_vote_comment(self):
        data = {"up": 1, "vote_id": 1, "method": "comment_vote"}
        data_down = {"down": 1, "vote_id": 1, "method": "comment_vote"}
        rating_start = PostComments.objects.get(id=data["vote_id"]).rating
        response = self.client.post(reverse("poll:vote"), data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start + 1, msg="err vote up")
        response = self.client.post(reverse("poll:vote"), data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote up double")
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg="err vote down")
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(
            rating, rating_start - 1, msg="err vote down double after plus"
        )
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote down double")

class TestVotes(TestCase):
    fixtures = ['users.json', 'tags.json', 'posts.json', 'comment.json']
    def setUp(self):
        data = {"username": "testuser", "password": "123456789iI"}
        self.client = Client()
        self.user = Profile.objects.get(username=data["username"])
        self.client.force_login(self.user)

    def test_vote_post(self):
        data = {"up": 1, "vote_id": 1, "method": "post_vote"}
        data_down = {"down": 1, "vote_id": 1, "method": "post_vote"}
        rating_start = Post.objects.get(id=data["vote_id"]).votes
        response = self.client.post(reverse("poll:vote"), data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start + 1, msg="err vote up")
        response = self.client.post(reverse("poll:vote"), data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote up double")
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg="err vote down")
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(
            rating, rating_start - 1, msg="err vote down double after plus"
        )
        response = self.client.post(reverse("poll:vote"), data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, "err", msg="err vote down double")

    def test_best_comment(self):
        data = {"comment_id": 14}
        response = self.client.post(reverse("poll:best_choice"), data=data)
        bests = PostComments.objects.get(id=data["comment_id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bests.best)
        data_new = {"comment_id": 13}
        response = self.client.post(reverse("poll:best_choice"), data=data_new)
        bests = PostComments.objects.get(id=data_new["comment_id"]).best
        ex_best = PostComments.objects.get(id=data["comment_id"]).best
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bests)
        self.assertFalse(ex_best)

    def test_forbidden_best(self):
        data = {"comment_id": 1}
        response = self.client.post(reverse("poll:best_choice"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestSearchTags(TestCase):
    fixtures = ['users.json', 'tags.json', 'posts.json', 'comment.json']
    def setUp(self):
        data = {"username": "testuser", "password": "123456789iI"}
        self.client = Client()
        self.user = Profile.objects.get(username=data["username"])
        self.client.force_login(self.user)

    def test_search(self):
        data = {"search": "Lorem ipsum"}
        response = self.client.post(reverse("poll:search"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = response._container[0].decode()
        self.assertTrue("Where can I get some?" in request)

    def test_tags(self):
        data = {"post_tag": "hello, name, test, what"}
        data_true = {"post_tag": "hello, name, test"}
        form = Tags(data=data)
        self.assertFalse(form.is_valid())
        form = Tags(data=data_true)
        self.assertTrue(form.is_valid())

    def test_search_tags(self):
        data = {"tag": "django"}
        response = self.client.post(reverse("poll:search"), data=data)
        self.assertTrue("How are you doing?" in response._container[0].decode())
