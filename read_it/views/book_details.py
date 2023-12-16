from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Book, Genre


def book_details(request: HttpRequest, id: int) -> HttpResponse:
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    context = {"book": book, "genres": book.genres.order_by(Genre.name.field.name).all()}
    return render(
        request,
        "book_details.html",
        context=context,
    )
