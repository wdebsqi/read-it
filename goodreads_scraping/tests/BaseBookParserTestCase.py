from pathlib import Path

from django.test import TestCase as DjangoTestCase


class BaseBookParserTestCase(DjangoTestCase):
    databases = {"test"}

    def setUp(self):
        with open(Path(__file__).parent / "example_book_page.html", "r") as f:
            self.test_html = f.read()
