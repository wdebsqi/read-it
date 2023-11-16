from django.db import models

from .GoodreadsAuthorPage import GoodreadsAuthorPage
from .GoodreadsBookPage import GoodreadsBookPage


class GoodreadsBookAuthor(models.Model):
    book = models.ForeignKey(GoodreadsBookPage, on_delete=models.CASCADE)
    author = models.ForeignKey(GoodreadsAuthorPage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "goodreads_book_author"
