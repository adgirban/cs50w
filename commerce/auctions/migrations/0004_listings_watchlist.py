# Generated by Django 4.1.5 on 2023-12-17 14:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_listings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='userWatchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
