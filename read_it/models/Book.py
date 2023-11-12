import json
from datetime import datetime

from django.core.validators import MinLengthValidator
from django.db import models

from goodreads_scraping.models import GoodreadsBookPage

from .Author import Author
from .Genre import Genre


class Book(models.Model):
    title = models.CharField(max_length=150, blank=False)
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13)], default="", blank=True)
    published_on = models.DateField(null=True, blank=True)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    goodreads_book_page = models.ForeignKey(
        GoodreadsBookPage, on_delete=models.CASCADE, blank=True, null=True
    )
    authors = models.ManyToManyField(Author, through="BookAuthor")
    genres = models.ManyToManyField(Genre, through="BookGenre")

    class Meta:
        db_table = "book"

    def __str__(self):
        return json.dumps(
            {
                "title": self.title,
                "isbn": self.isbn,
                "published_on": datetime.strftime(self.published_on, "%Y-%m-%d"),
                "description": self.description[:100],
            },
            indent=2,
        )
