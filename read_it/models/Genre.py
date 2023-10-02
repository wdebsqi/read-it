from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=150, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genre"

    def __str__(self):
        return self.name
