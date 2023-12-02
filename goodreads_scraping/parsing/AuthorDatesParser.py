from datetime import datetime
from lxml import etree
from typing import Tuple

from .BaseParser import BaseParser


class AuthorDatesParser(BaseParser):
    def __init__(self, html):
        self.xml = etree.fromstring(html)

    def get_xpath(self, event_name: str) -> str:
        return (
            "//div[@class='mainContentContainer']"
            + "//div[@class='mainContentFloat']"
            + "//div[@class='rightContainer']"
            + "//div[@class='dataItem' and @itemprop='{}']".format(event_name)
        )

    def parse(self) -> Tuple[datetime, datetime] | Tuple[datetime, None] | Tuple[None, None]:
        return self._parse_helper("birthDate"), self._parse_helper("deathDate")

    def _parse_helper(self, event_name: str) -> datetime:
        xpath_match = self.xml.xpath(self.get_xpath(event_name))
        if not xpath_match:
            return

        xpath_match_birth_date = xpath_match[0]
        text_lines_birth_date = xpath_match_birth_date.itertext()
        joined_text_lines_birth_date = "\n".join(text_lines_birth_date).strip()
        datetime_birth_date = datetime.strptime(joined_text_lines_birth_date, "%B %d, %Y")
        return datetime_birth_date
