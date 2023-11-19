import re

from lxml import etree

from .BaseParser import BaseParser


class AuthorIdsFromBookPageParser(BaseParser):
    def __init__(self, html: str) -> None:
        self._html_tree = etree.fromstring(html)

    def get_xpath(self) -> str:
        return "//div[@class='ContributorLinksList']//a[@class='ContributorLink']"

    def parse(self) -> list[int]:
        xpath_matches = self._html_tree.xpath(self.get_xpath())
        parsed_ids = []
        for match in xpath_matches:
            url = match.attrib["href"]
            parsed_ids.append(self._extract_author_id_from_url(url))
        return parsed_ids

    def _extract_author_id_from_url(self, url: str) -> int | None:
        id_matching_regexp = r"https://www.goodreads.com/author/show/(\d+)"
        matches = re.findall(id_matching_regexp, url)
        if not matches:
            return None
        return int(matches[0])
