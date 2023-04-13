from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testUser", email="test@test.com", password="secret"
        )

        cls.post = Post.objects.create(title="title", body="body", author=cls.user)

    def test_post_model(self):
        self.assertEqual(self.post.title, "title")
        self.assertEqual(self.post.body, "body")
        self.assertEqual(self.post.author.username, "testUser")
        self.assertEqual(str(self.post), "title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_listview_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_detailview_url(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "body")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "title")
        self.assertTemplateUsed(response, "post_detail.html")
