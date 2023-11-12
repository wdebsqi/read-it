import re

import requests as r
from bs4 import BeautifulSoup

from ...models import GoodreadsBookPage


class Scraper:
    BASE_URL = "http://goodreads.com/book/show/"

    def scrape(self, book_id: int) -> GoodreadsBookPage:
        """Scrapes the HTML for a given book_id."""

        url = f"{self.BASE_URL}{book_id}"
        response = r.get(url)

        return self._map_http_response_to_result(response)

    def _map_http_response_to_result(self, response: r.Response) -> GoodreadsBookPage:
        """Maps the HTML response to the model class representing the scraping result."""

        result = GoodreadsBookPage()
        result.url = response.url
        result.http_status_code = response.status_code
        result.headers = response.headers

        html = BeautifulSoup(response.content, "html.parser")
        result.title = str(html.title.string)
        result.website_content = self._remove_redundant_tags(html)
        return result

    def _remove_redundant_tags(self, html: BeautifulSoup | None) -> str | None:
        """Removes the <style> and <script> tags and the entire content inside them
        to decrease the size of the HTML. If there are any extra whitespaces left, also removes them."""

        if not html:
            return

        for tag in html(["style", "script"]):
            tag.decompose()

        return re.sub(r"\s+", " ", str(html))
