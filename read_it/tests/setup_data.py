from ..models import Book


def create_new_book(id: int | None = None) -> Book:
    return Book.objects.create(
        id=id,
        title=f"This is a test book number {id}",
        description="This is a test description number",
        published_on="2021-01-01",
    )
