from django.contrib import admin

from ..models import BookAuthor, BookGenre


class BookAuthorAdminInline(admin.TabularInline):
    model = BookAuthor


class BookGenreAdminInline(admin.TabularInline):
    model = BookGenre
