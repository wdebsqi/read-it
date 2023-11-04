from lxml import etree

from read_it.models import Genre

from .BaseParser import BaseParser


class BookGenreParser(BaseParser):
    def __init__(self, html: str) -> None:
        self._html_tree = etree.fromstring(html)

    def get_xpath(self) -> str:
        return (
            "//div[@data-testid='genresList']"
            + "//span[@class='BookPageMetadataSection__genreButton']"
            + "//span[@class='Button__labelItem']"
        )

    def parse(self) -> list[Genre]:
        genre_names = []
        xpath_matches = self._html_tree.xpath(self.get_xpath())

        for xpath_match in xpath_matches:
            genre_names.append(xpath_match.text)

        return self._get_genres_based_on_genre_names(genre_names)

    def _get_genres_based_on_genre_names(self, genre_names: list[str]) -> list[Genre]:
        genres = []
        for genre_name in genre_names:
            genre_matched_in_db = Genre.objects.filter(name=genre_name).first()
            if genre_matched_in_db:
                genres.append(genre_matched_in_db)
            else:
                genres.append(Genre(name=genre_name))

        return genres
