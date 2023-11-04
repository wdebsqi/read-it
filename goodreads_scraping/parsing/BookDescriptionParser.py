from lxml.etree import Element

from .BaseParser import BaseParser


class BookDescriptionParser(BaseParser):
    def get_xpath(self) -> str:
        return "//div[@data-testid='description']"

    def parse(self, xml: Element) -> str:
        xpath_match = xml.xpath(self.get_xpath())[0]
        text_lines = xpath_match.itertext()
        return "\n".join(text_lines)
