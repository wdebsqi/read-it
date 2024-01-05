from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Book


def home(request: HttpRequest) -> HttpResponse:
    last_published_books = Book.objects.order_by(f"-{Book.published_on.field.name}").all()[:5]

    context = {"last_published_books": last_published_books}
    return render(request, "home.html", context=context)
