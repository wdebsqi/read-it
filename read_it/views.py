from django.http import Http404
from django.shortcuts import render

from .models import Book


def book_details(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, "read_it/book_details.html", {"book": book})
