from django.test import Client, TestCase
from django.urls import reverse

from ..models import Book
from .setup_data import create_new_book


class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            create_new_book()

        cls.client = Client()

    def test_home_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_context_contains_five_books(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["last_published_books"]), 5)

    def test_home_context_contains_no_books_when_db_empty(self):
        Book.objects.all().delete()
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["last_published_books"]), 0)
