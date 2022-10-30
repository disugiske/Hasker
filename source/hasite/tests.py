import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from hasite.forms import AddPost, Tags, AddCommentForm
from hasite.models import PostTags, Post, PostComments


class TestPages(TestCase):

    def test_index(self):
        response = self.client.get(reverse("hasker:index"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("hasker:index_hot"))
        self.assertEqual(response.status_code, 200)

    def test_auth_req(self):
        self.client = Client()
        response = self.client.get(reverse("hasker:account"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("hasker:addpost"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/?next=/addpost/')

    def test_auth_register(self):
        response = self.client.get(reverse("hasker:auth"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("hasker:register"))
        self.assertEqual(response.status_code, 200)


class TestFormsVote(TestCase):
    fixtures = [
        'user.json',
        'post.json',
        'comments.json'
    ]

    def setUp(self):
        data = {'username': 'testuser', 'password': '123456789iI'}
        self.client = Client()
        self.client.post(path="/auth/", data=data)
        self.user = User.objects.get(username=data['username'])

    def test_page(self):
        response = self.client.get(reverse("hasker:addpost"))
        self.assertEqual(response.status_code, 200)

    def test_addpost(self):
        data = {'title': 'whats up?', 'text': 'Lorem ipsum'}
        form = AddPost(data=data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            post = Post.objects.create(author=self.user, title=data['title'], text=data['text'])
            response = self.client.get(f'/post/{post.id}')
            self.assertEqual(response.status_code, 200)

    def test_tags(self):
        data = {'post_tag': 'hello, name, test, what'}
        form = Tags(data=data)
        self.assertFalse(form.is_valid())

    def test_add_comment(self):
        data = {'title': 'whats up?', 'text': 'Lorem ipsum'}
        post = Post.objects.create(author=self.user, title=data['title'], text=data['text'])
        response = self.client.post(path=f"/post/{post.id}",
                                    data={'comment': 'hello world', 'comment_author': self.user})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/post/{post.id}")

    def test_vote_comment(self):
        data = {
            "up": 1,
            "vote_id": 1,
            "method": "comment_vote"
        }
        data_down = {
            "down": 1,
            "vote_id": 1,
            "method": "comment_vote"}
        rating_start = PostComments.objects.get(id=data['vote_id']).rating
        response = self.client.post(path='/vote', data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start+1, msg='err vote up')

        response = self.client.post(path='/vote', data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, 'err', msg='err vote up double')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg='err vote down')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start - 1, msg='err vote down double after plus')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, 'err', msg='err vote down double')

    def test_vote_post(self):
        data = {
            "up": 1,
            "vote_id": 1,
            "method": "post_vote"
        }
        data_down = {
            "down": 1,
            "vote_id": 1,
            "method": "post_vote"}
        rating_start = Post.objects.get(id=data['vote_id']).votes
        response = self.client.post(path='/vote', data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start + 1, msg='err vote up')

        response = self.client.post(path='/vote', data=data)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, 'err', msg='err vote up double')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start, msg='err vote down')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, rating_start - 1, msg='err vote down double after plus')

        response = self.client.post(path='/vote', data=data_down)
        rating = json.loads(response._container[0].decode())
        rating = rating.get("rating")
        self.assertEqual(rating, 'err', msg='err vote down double')

    def test_best_comment(self):
        data = {"comment_id": 14}
        response = self.client.post(path='/best/', data=data)

        bests = PostComments.objects.get(id=data['comment_id'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bests.best)

        data_new = {"comment_id": 13}
        response = self.client.post(path='/best/', data=data_new)
        bests = PostComments.objects.get(id=data_new['comment_id']).best
        ex_best = PostComments.objects.get(id=data['comment_id']).best
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bests)
        self.assertFalse(ex_best)

    def test_forbidden_best(self):
        data = {"comment_id": 1}
        response = self.client.post(path='/best/', data=data)
        self.assertEqual(response.status_code, 403)