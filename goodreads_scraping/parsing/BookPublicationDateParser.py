import re
from datetime import datetime

from lxml.etree import Element

from .BaseParser import BaseParser


class BookPublicationDateParser(BaseParser):
    DATE_MATCHING_REGEXP = r"\w+ \d{1,2}, \d{4}$"

    def get_xpath(self) -> str:
        return "//p[@data-testid='publicationInfo']"

    def parse(self, xml: Element) -> datetime:
        xpath_match = xml.xpath(self.get_xpath())[0]
        text_publication_date = re.findall(self.DATE_MATCHING_REGEXP, xpath_match.text)[0]
        return datetime.strptime(text_publication_date, "%B %d, %Y")
