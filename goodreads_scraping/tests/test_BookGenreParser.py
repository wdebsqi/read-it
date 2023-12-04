from ..parsing import BookGenreParser
from . import BaseBookParserTestCase


class BookGenreParserTest(BaseBookParserTestCase):
    def setUp(self):
        super().setUp()
        self.parser = BookGenreParser(self.test_html)
        self.correct_genres = [
            "Fantasy",
            "Classics",
            "Fiction",
            "Adventure",
            "High Fantasy",
            "Science Fiction Fantasy",
            "Epic Fantasy",
        ]

    def test_parse_genres_from_html(self):
        parsed_genres = self.parser.parse_genre_names()
        self.assertEquals(len(parsed_genres), len(self.correct_genres))

        for genre_name in parsed_genres:
            self.assertIn(genre_name, self.correct_genres)
