from django.contrib import admin

from .inlines import BookAuthorAdminInline


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_names")
    inlines = (BookAuthorAdminInline,)
