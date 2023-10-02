from django.contrib import admin

from ..models import Author, Book, Genre
from .AuthorAdmin import AuthorAdmin
from .BookAdmin import BookAdmin

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
