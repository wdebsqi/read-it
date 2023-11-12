import logging

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from goodreads_scraping.models import GoodreadsBookPage
from read_it.models import Book

from ...parsing import BookGenreParser, BookParser

logger = logging.getLogger("db")


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        scraping_results_to_parse = self._get_records_not_parsed_with_current_parser()

        for scraping_result in scraping_results_to_parse:
            try:
                logger.info(f"Trying to parse {GoodreadsBookPage.__name__} with id {scraping_result.id}...")
                book_parser = BookParser(scraping_result.website_content)
                genre_parser = BookGenreParser(scraping_result.website_content)
                parsed_book = book_parser.parse()
                genres = genre_parser.parse()
                for genre in genres:
                    genre.save()

                already_parsed_book_in_db = Book.objects.filter(goodreads_book_page=scraping_result).first()
                if already_parsed_book_in_db:
                    logger.info(
                        f"Parsed book already exists for this {GoodreadsBookPage.__name__}."
                        + "Trying to update it..."
                    )
                    already_parsed_book_in_db.title = parsed_book.title
                    already_parsed_book_in_db.description = parsed_book.description
                    already_parsed_book_in_db.published_on = parsed_book.published_on
                    already_parsed_book_in_db.save()
                    already_parsed_book_in_db.genres.add(*genres)
                else:
                    logger.info(
                        f"No parsed book exist for this {GoodreadsBookPage.__name__}."
                        + "Trying to save a new one..."
                    )
                    parsed_book.goodreads_book_page = scraping_result
                    parsed_book.save()
                    parsed_book.genres.add(*genres)

                logger.info(f"Updating {GoodreadsBookPage.__name__}.parser_version...")
                scraping_result.parser_version = BookParser.VERSION
                scraping_result.parsed_at = timezone.now()
                scraping_result.save()
            except Exception as e:
                logger.error(e)

    def _get_records_not_parsed_with_current_parser(self) -> list[GoodreadsBookPage]:
        return GoodreadsBookPage.objects.filter(
            Q(parser_version__lt=BookParser.VERSION) | Q(parser_version__isnull=True)
        )
