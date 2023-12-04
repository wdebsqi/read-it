# Generated by Django 4.2.5 on 2023-12-03 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodreads_scraping', '0005_alter_goodreadsauthorpage_url_and_more'),
        ('read_it', '0005_alter_author_middle_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='goodreads_author_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goodreads_scraping.goodreadsauthorpage'),
        ),
    ]
