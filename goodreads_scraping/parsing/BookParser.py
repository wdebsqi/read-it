from lxml import etree

from read_it.models import Book

from .BookDescriptionParser import BookDescriptionParser
from .BookPublicationDateParser import BookPublicationDateParser
from .BookTitleParser import BookTitleParser


class BookParser:
    VERSION = 1

    def __init__(self, html: str) -> None:
        self._html_tree = etree.fromstring(html)
        self.title_parser = BookTitleParser()
        self.description_parser = BookDescriptionParser()
        self.publication_date_parser = BookPublicationDateParser()

    def parse(self) -> Book:
        title = self.title_parser.parse(self._html_tree)
        description = self.description_parser.parse(self._html_tree)
        published_on = self.publication_date_parser.parse(self._html_tree)

        return Book(title=title, description=description, published_on=published_on)
