from datetime import datetime

from read_it.models import Author

from ..parsing import AuthorParser
from . import BaseAuthorParserTestCase


class BookParserTest(BaseAuthorParserTestCase):
    def setUp(self):
        super().setUp()
        self.parser = AuthorParser(self.test_html)
        self.correctly_parsed_author_info = Author(
            first_name="J.R.R.",
            middle_names=None,
            last_name="Tolkien",
            birth_date=datetime.strptime("January 03, 1892", "%B %d, %Y"),
            death_date=datetime.strptime("September 02, 1973", "%B %d, %Y"),
        )

    def test_parse_book_from_html(self):
        parsed_author = self.parser.parse()
        self.assertEquals(parsed_author.first_name, self.correctly_parsed_author_info.first_name)
        self.assertEquals(parsed_author.middle_names, self.correctly_parsed_author_info.middle_names)
        self.assertEquals(parsed_author.last_name, self.correctly_parsed_author_info.last_name)
        self.assertEquals(parsed_author.birth_date, self.correctly_parsed_author_info.birth_date)
        self.assertEquals(parsed_author.death_date, self.correctly_parsed_author_info.death_date)
