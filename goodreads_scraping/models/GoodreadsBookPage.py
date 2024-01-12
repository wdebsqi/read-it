import json

from django.db import models

from .GoodreadsAuthorPage import GoodreadsAuthorPage


class GoodreadsBookPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(blank=False, max_length=200, unique=True)
    http_status_code = models.IntegerField(blank=False)
    title = models.CharField(max_length=200)
    headers = models.TextField()
    website_content = models.TextField()
    parser_version = models.IntegerField(default=0)
    parsed_at = models.DateTimeField(null=True)
    authors = models.ManyToManyField(GoodreadsAuthorPage, through="GoodreadsBookAuthor")

    class Meta:
        db_table = "goodreads_book_page"

    def __str__(self) -> str:
        return json.dumps(
            {
                "url": self.url,
                "http_status_code": self.http_status_code,
                "title": self.title,
                "website_content": self.website_content[0:100],
                "parser_version": self.parser_version,
                "parsed_at": self.parsed_at.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_at else None,
            },
            indent=2,
        )
