import json

from django.db import models


class GoodreadsScrapingResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(blank=False, max_length=200)
    http_status_code = models.IntegerField(blank=False)
    title = models.CharField(max_length=200)
    headers = models.TextField()
    website_content = models.TextField()

    class Meta:
        db_table = "goodreads_scraping_result"

    def __str__(self) -> str:
        return json.dumps(
            {
                "url": self.url,
                "http_status_code": self.http_status_code,
                "title": self.title,
                "website_content": self.website_content[0:100],
                "headers": dict(self.headers),
            },
            indent=2,
        )
