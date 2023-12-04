from django.db import models
from goodreads_scraping.models import GoodreadsAuthorPage


class Author(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    middle_names = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    goodreads_author_page = models.ForeignKey(GoodreadsAuthorPage, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "author"

    def __str__(self):
        names_to_consider = [self.first_name]
        if self.middle_names:
            names_to_consider.append(self.middle_names)
        names_to_consider.append(self.last_name)
        return " ".join(names_to_consider)
