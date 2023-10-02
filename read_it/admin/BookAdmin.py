from django.contrib import admin

from .inlines import BookAuthorAdminInline, BookGenreAdminInline


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "published_on")
    inlines = (BookAuthorAdminInline, BookGenreAdminInline)
