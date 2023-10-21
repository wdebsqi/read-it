import logging
from random import randint, random
from time import sleep
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from ...models import GoodreadsScrapingResult
from .Scraper import Scraper

logger = logging.getLogger("db")

MAX_UPPER_ID_TO_SCRAPE = 1_000_000
MAX_SECONDS_TO_WAIT = 120


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            help="The number of pages that will be scraped",
            type=int,
            required=True,
        )

        parser.add_argument("-s", "--start", help="The ID of the page to start from", type=int, default=1)
        parser.add_argument(
            "-o",
            "--overwrite",
            help="Whether to overwrite the previously scraped results",
            action="store_true",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        scraper = Scraper()
        start, number, overwrite = options["start"], options["number"], options["overwrite"]

        ids_to_scrape = self._get_random_ids_to_scrape(start=start, size=number)

        for id in ids_to_scrape:
            self._wait_random_time()
            logger.info(f"Trying to scrape a book with id {id}")

            try:
                result = scraper.scrape(id)
            except Exception as e:
                logger.error(e)
                continue

            match = GoodreadsScrapingResult.objects.filter(url__exact=result.url).first()
            if not match:
                logging.info(f"No previously existing record for a book with {id} found, creating a new one")
                try:
                    result.save()
                    logging.info(f"Successfully saved the result from {result.url}")
                except Exception as e:
                    logger.error(e)
                continue

            if overwrite:
                logging.info(f"Previously existing record for a book with {id} found, overwriting it")
                match.created_at = result.created_at
                match.http_status_code = result.http_status_code
                match.title = result.title
                match.headers = result.headers
                match.website_content = result.website_content
                try:
                    match.save()
                    logging.info(f"Successfully saved the result from {result.url}")
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
