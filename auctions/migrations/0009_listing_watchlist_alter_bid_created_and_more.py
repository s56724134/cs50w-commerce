# Generated by Django 4.2.6 on 2023-10-23 13:52

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_created_alter_listing_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='listingWatchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 21, 52, 50, 469678)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 21, 52, 50, 468678)),
        ),
    ]
