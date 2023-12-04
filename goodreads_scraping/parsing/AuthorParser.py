from lxml import etree

from read_it.models import Author

from .AuthorNamesParser import AuthorNamesParser
from .AuthorDatesParser import AuthorDatesParser


class AuthorParser:
    VERSION = 1

    def __init__(self, html: str) -> None:
        self.names_parser = AuthorNamesParser(html)
        self.dates_parser = AuthorDatesParser(html)

    def parse(self) -> Author:
        first_name, middle_names, last_name = self.names_parser.parse()
        birth_date, death_date = self.dates_parser.parse()

        return Author(
            first_name=first_name, middle_names=middle_names, last_name=last_name, birth_date=birth_date, death_date=death_date
        )
