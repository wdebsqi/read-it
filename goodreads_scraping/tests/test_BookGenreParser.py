from read_it.models import Genre

from ..parsing import BookGenreParser
from . import BaseParserTestCase


class BookGenreParserTest(BaseParserTestCase):
    databases = "__all__"

    def setUp(self):
        super().setUp()
        self.parser = BookGenreParser(self.test_html)
        self.correct_genres = [
            Genre(name="Fantasy"),
            Genre(name="Classics"),
            Genre(name="Fiction"),
            Genre(name="Adventure"),
            Genre(name="High Fantasy"),
            Genre(name="Science Fiction Fantasy"),
            Genre(name="Epic Fantasy"),
        ]

    def test_parse_genres_from_html(self):
        parsed_genres = self.parser.parse()
        self.assertEquals(len(parsed_genres), len(self.correct_genres))

        parsed_genre_names = self._extract_distinct_names_from_genres(parsed_genres)
        correct_genre_names = self._extract_distinct_names_from_genres(self.correct_genres)

        for genre_name in parsed_genre_names:
            self.assertIn(genre_name, correct_genre_names)

    def _extract_distinct_names_from_genres(self, genres: list[Genre]) -> set[str]:
        return set(genre.name for genre in genres)
