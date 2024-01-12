from datetime import datetime

from lxml import etree

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

    def parse(self) -> tuple[datetime | None, datetime | None]:
        return self._parse_date_from_the_chosen_div("birthDate"), self._parse_date_from_the_chosen_div("deathDate")

    def _parse_date_from_the_chosen_div(self, event_name: str) -> datetime | None:
        xpath_match = self.xml.xpath(self.get_xpath(event_name))
        if not xpath_match:
            return

        xpath_match_birth_date = xpath_match[0]
        text_lines_birth_date = xpath_match_birth_date.text.strip()
        datetime_birth_date = datetime.strptime(text_lines_birth_date, "%B %d, %Y")
        return datetime_birth_date
