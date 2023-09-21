from datetime import datetime

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=200)
    published = models.DateField()
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = "book"

    def __str__(self):
        return f"book({self.title}, {self.published}"
