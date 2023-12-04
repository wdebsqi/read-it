from datetime import datetime

from read_it.models import Book

from ..parsing import BookParser
from . import BaseBookParserTestCase


class BookParserTest(BaseBookParserTestCase):
    def setUp(self):
        super().setUp()
        self.parser = BookParser(self.test_html)
        self.correctly_parsed_book_info = Book(
            title="The Fellowship of the Ring",
            description="This is a description of one of most iconic books",  # noqa: E501
            published_on=datetime.strptime("July 29, 1954", "%B %d, %Y"),
        )

    def test_parse_book_from_html(self):
        parsed_book = self.parser.parse()
        self.assertEquals(parsed_book.title, self.correctly_parsed_book_info.title)
        self.assertEquals(
            parsed_book.description.strip(), self.correctly_parsed_book_info.description.strip()
        )
        self.assertEquals(parsed_book.published_on, self.correctly_parsed_book_info.published_on)
