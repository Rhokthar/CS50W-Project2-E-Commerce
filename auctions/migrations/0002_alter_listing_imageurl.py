# Generated by Django 4.0.6 on 2022-08-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageURL',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='Image URL'),
        ),
    ]
