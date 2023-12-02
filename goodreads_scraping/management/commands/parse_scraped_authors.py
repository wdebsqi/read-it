import logging

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from goodreads_scraping.models import GoodreadsAuthorPage
from read_it.models import Author

from ...parsing import BookParser, AuthorParser

logger = logging.getLogger("db")


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        scraping_results_to_parse = self._get_records_not_parsed_with_current_parser()

        for scraping_result in scraping_results_to_parse:
            try:
                logger.info(f"Trying to parse {GoodreadsAuthorPage.__name__} with id {scraping_result.id}...")
                author_parser = AuthorParser(scraping_result.website_content)
                parsed_author = author_parser.parse()

                already_parsed_author_in_db = Author.objects.filter(goodreads_book_page=scraping_result).first()
                if already_parsed_author_in_db:
                    logger.info(
                        f"Parsed book already exists for this {GoodreadsAuthorPage.__name__}." + "Trying to update it..."
                    )
                    already_parsed_author_in_db.title = parsed_author.title
                    already_parsed_author_in_db.description = parsed_author.description
                    already_parsed_author_in_db.published_on = parsed_author.published_on
                    already_parsed_author_in_db.save()
                else:
                    logger.info(f"No parsed book exist for this {GoodreadsAuthorPage.__name__}." + "Trying to save a new one...")
                    parsed_author.goodreads_book_page = scraping_result
                    parsed_author.save()

                logger.info(f"Updating {GoodreadsAuthorPage.__name__}.parser_version...")
                scraping_result.parser_version = BookParser.VERSION
                scraping_result.parsed_at = timezone.now()
                scraping_result.save()
            except Exception as e:
                logger.error(e)

    def _get_records_not_parsed_with_current_parser(self) -> list[GoodreadsAuthorPage]:
        return GoodreadsAuthorPage.objects.filter(Q(parser_version__lt=AuthorParser.VERSION) | Q(parser_version__isnull=True))
