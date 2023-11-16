import logging
from random import randint, random
from time import sleep
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from ...models import GoodreadsAuthorPage, GoodreadsBookPage
from ...parsing import AuthorIdsFromBookPageParser
from .AuthorScraper import AuthorScraper
from .BookScraper import BookScraper

logger = logging.getLogger("db")

MAX_UPPER_ID_TO_SCRAPE = 1_000_000
MAX_SECONDS_TO_WAIT = 120


class Command(BaseCommand):
    book_scraper = BookScraper()
    author_scraper = AuthorScraper()

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            help="The number of book pages that will be scraped",
            type=int,
            required=True,
        )

        parser.add_argument(
            "-s", "--start", help="The ID of the book page to start from", type=int, default=1
        )
        parser.add_argument(
            "-o",
            "--overwrite",
            help="Whether to overwrite the previously scraped results",
            action="store_true",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        start, number, overwrite = options["start"], options["number"], options["overwrite"]

        book_ids_to_scrape = self._get_random_ids_to_scrape(start=start, size=number)

        for book_id in book_ids_to_scrape:
            self._wait_random_time()
            logger.info(f"Trying to scrape a book with id {book_id}")

            try:
                scraped_book_page = self.book_scraper.scrape(book_id)

                author_id_parser = AuthorIdsFromBookPageParser(scraped_book_page.website_content)
                authors_ids = author_id_parser.parse()
                scraped_authors_pages = [self.author_scraper.scrape(author_id) for author_id in authors_ids]
            except Exception as e:
                logger.error(e)
                continue

            authors_pages = self._handle_author_pages(scraped_authors_pages)
            book_page_in_db = GoodreadsBookPage.objects.filter(url__exact=scraped_book_page.url).first()
            if not book_page_in_db:
                logger.info(
                    f"No previously existing record for a book with {book_id} found, creating a new one"
                )
                try:
                    for author_page in authors_pages:
                        author_page.save()
                    scraped_book_page.save()
                    scraped_book_page.authors.add(*authors_pages)
                    logger.info(
                        f"Successfully saved the result from {scraped_book_page.url} "
                        + f"and: {[author_page.url for author_page in authors_pages]}"
                    )
                except Exception as e:
                    logger.error(e)
                continue

            if overwrite:
                logger.info(f"Previously existing record for a book with {book_id} found, overwriting it")

                book_page_in_db.created_at = scraped_book_page.created_at
                book_page_in_db.http_status_code = scraped_book_page.http_status_code
                book_page_in_db.title = scraped_book_page.title
                book_page_in_db.headers = scraped_book_page.headers
                book_page_in_db.website_content = scraped_book_page.website_content
                book_page_in_db.authors.add(*authors_pages)

                try:
                    book_page_in_db.save()
                    logger.info(
                        f"Successfully saved the result from {book_page_in_db.url} "
                        + f"and: {[author_page.url for author_page in authors_pages]}"
                    )
                except Exception as e:
                    logger.error(e)
                continue

    def _get_random_ids_to_scrape(self, start: int, size: int) -> set:
        """Creates a set of random IDs of books to scrape.
        The IDs will be drawn from the range(*start*, *MAX_UPPER_ID_TO_SCRAPE*).
        The number of IDs in the set can be controller with the *size* variable."""

        to_scrape = set()
        while len(to_scrape) < size:
            random_id = randint(start, MAX_UPPER_ID_TO_SCRAPE)
            to_scrape.add(random_id)

        return to_scrape

    def _wait_random_time(self) -> None:
        """Waits a random amount of time, between 0 and *MAX_SECONDS_TO_WAIT* seconds"""
        seconds_to_wait = random() * MAX_SECONDS_TO_WAIT
        logger.info(f"Will wait {seconds_to_wait} between scrapping another page.")
        sleep(seconds_to_wait)

    def _handle_author_pages(
        self, scraped_author_pages: list[GoodreadsAuthorPage]
    ) -> list[GoodreadsAuthorPage]:
        """Takes a list of scraped author pages and filters it to not contain new objects
        if there's an already existing record for the same url in the database.
        Thanks to this the scraped pages can be safely saved without worrying
        about the potential duplicate creation."""
        author_pages = []

        for scraped_author_page in scraped_author_pages:
            author_page_in_db = GoodreadsAuthorPage.objects.filter(url__exact=scraped_author_page.url).first()

            if not author_page_in_db:
                author_pages.append(scraped_author_page)
                continue

            author_page_in_db.created_at = scraped_author_page.created_at
            author_page_in_db.http_status_code = scraped_author_page.http_status_code
            author_page_in_db.title = scraped_author_page.title
            author_page_in_db.headers = scraped_author_page.headers
            author_page_in_db.website_content = scraped_author_page.website_content
            author_pages.append(author_page_in_db)

        return author_pages
