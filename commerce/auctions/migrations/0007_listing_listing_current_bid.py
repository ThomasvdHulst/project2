# Generated by Django 4.0.6 on 2023-01-28 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_listing_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_current_bid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
