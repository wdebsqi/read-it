from pathlib import Path

from django.test import TestCase as DjangoTestCase


class BaseAuthorParserTestCase(DjangoTestCase):
    databases = {"test"}

    def setUp(self):
        with open(Path(__file__).parent / "example_author_page.html", "r", encoding='utf-8') as f:
            self.test_html = f.read()
