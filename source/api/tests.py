from django.test import TestCase


class TestPages(TestCase):
    def test_swagger(self):
        response = self.client.get("/swagger/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/redoc/")
        self.assertEqual(response.status_code, 200)

    def testapi(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, 200)


class TestAPI(TestCase):
    fixtures = ["users.json", "posts.json", "comment.json"]

    def test_index(self):
        response = self.client.get("/api/v1/index/?format=json")
        result = response.json().get('results')
        self.assertTrue(result)
        self.assertTrue(result[0].get('author') == "admin")
        self.assertTrue(result[1].get('title') == "The standard Lorem Ipsum passage, used since the 1500s")
        self.assertTrue(result[5].get('comments') == "1")

    def test_indexhot(self):
        response = self.client.get("/api/v1/indexhot/?format=json")
        result = response.json().get('results')
        self.assertTrue(result)
        self.assertTrue(response.json().get('count') == 6)
        self.assertTrue(result[0].get('author') == "admin")
        self.assertTrue(result[1].get('title') == "Why do we use it?")
        self.assertTrue(result[5].get('comments') == "1")

    def test_post(self):
        test_result = {
            "id": 1,
            "title": "What is Lorem Ipsum?",
            "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "author": "admin",
            "votes": 0
        }
        response = self.client.get("/api/v1/post/1/?format=json")
        result = response.json()
        self.assertEqual(result, test_result)

    def test_trends(self):
        response = self.client.get("/api/v1/trending/?format=json").json()
        self.assertTrue(response)
        self.assertTrue(len(response)<=20)
        self.assertEqual(response[0].get('title'), "1914 translation by H. Rackham")

    def test_comments(self):
        response = self.client.get("/api/v1/post/1/comments/?format=json").json()
        self.assertTrue(response)
        self.assertEqual(len(response), 1)
        response = self.client.get("/api/v1/post/2/comments/?format=json").json()
        self.assertFalse(response)
        self.assertEqual(len(response), 0)
        response = self.client.get("/api/v1/post/6/comments/?format=json").json()
        self.assertEqual(len(response), 2)

    def test_search(self):
        response = self.client.get("/api/v1/search/?format=json&word=lorem").json()
        self.assertTrue(response)
        self.assertEqual(response.get('count'), 5)
        response = self.client.get("/api/v1/search/?format=json&word=where").json()
        self.assertTrue(response)
        self.assertEqual(response.get('count'), 2)
        response = self.client.get("/api/v1/search/?format=json&tag=django").json()
        self.assertTrue(response)
        self.assertEqual(response.get('count'), 0)
        response = self.client.get("/api/v1/search/?format=json&tag=python").json()
        self.assertTrue(response)
        self.assertEqual(response.get('count'), 1)