from django.core.validators import MinLengthValidator
from django.db import models

from .Author import Author
from .Genre import Genre


class Book(models.Model):
    title = models.CharField(max_length=150, blank=False)
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13)], default="", blank=True)
    published_on = models.DateField(null=True, blank=True)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Author, through="BookAuthor")
    genres = models.ManyToManyField(Genre, through="BookGenre")

    class Meta:
        db_table = "book"

    def __str__(self):
        return self.title
