# Generated by Django 4.2.5 on 2023-11-12 12:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("read_it", "0003_book_goodreads_scraping_result"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="goodreads_scraping_result",
            new_name="goodreads_book_page",
        ),
    ]
