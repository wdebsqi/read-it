from lxml.etree import Element

from .BaseParser import BaseParser


class BookTitleParser(BaseParser):
    def get_xpath(self) -> str:
        return "//h1[@data-testid='bookTitle']"

    def parse(self, xml: Element) -> str:
        return xml.xpath(self.get_xpath())[0].text
