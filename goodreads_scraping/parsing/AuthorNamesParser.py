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
        xpath_match = self.xml.xpath(self.get_xpath)
        if not xpath_match:
            raise ValueError("Could not parse author names" + " from xpath: " + self.get_xpath + " in html")
        return xpath_match[0].text

    def get_first_name(self) -> str:
        return self.parsed_author_names.split()[0]

    def get_middle_names(self) -> str | None:
        if len(self.parsed_author_names.split()) > 2:
            return " ".join(self.parsed_author_names.split()[1:-1])

    def get_last_name(self) -> str:
        if len(self.parsed_author_names.split()) < 2:
            raise ValueError("Could not parse author last name" + " from xpath: " + self.get_xpath + " in html")
        return self.parsed_author_names.split()[-1]
