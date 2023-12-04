from lxml import etree

from .BaseParser import BaseParser


class AuthorNamesParser(BaseParser):
    def __init__(self, html):
        self.xml = etree.fromstring(html)
        self.parsed_author_names = self._parse_names()

    @property
    def get_xpath(self) -> str:
        return "//div[@class='mainContentContainer']" + "//div[@class='rightContainer']" + "//div//h1//span"

    def parse(self) -> tuple[str, str] | tuple[str, str, str]:
        return (self.get_first_name(), self.get_middle_names(), self.get_last_name())

    def _parse_names(self) -> str:
        xpath_match = self.xml.xpath(self.get_xpath)[0]
        text_lines = xpath_match.itertext()
        return "\n".join(text_lines)

    def get_first_name(self) -> str:
        return self.parsed_author_names.split()[0]

    def get_middle_names(self) -> str | None:
        if len(self.parsed_author_names.split()) > 2:
            return " ".join(self.parsed_author_names.split()[1:-1])

    def get_last_name(self) -> str:
        return self.parsed_author_names.split()[-1]
