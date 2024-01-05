from django.test import Client, TestCase
from django.urls import reverse

from .setup_data import create_new_book


class BookDetailsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_book = create_new_book()

        cls.client = Client()

    def test_book_details_view_returns_200_if_book_exists(self):
        response = self.client.get(reverse("book_details", kwargs={"id": self.test_book.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_details_view_context_contains_book_data(self):
        response = self.client.get(reverse("book_details", kwargs={"id": self.test_book.id}))
        self.assertIsNotNone(getattr(response.context["book"], "title"))
        self.assertIsNotNone(getattr(response.context["book"], "description"))
        self.assertIsNotNone(getattr(response.context["book"], "published_on"))

    def test_book_details_view_returns_404_if_book_does_not_exist(self):
        response = self.client.get(reverse("book_details", kwargs={"id": self.test_book.id + 1}))
        self.assertEqual(response.status_code, 404)
