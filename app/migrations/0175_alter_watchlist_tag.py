# Generated by Django 5.0.3 on 2024-09-16 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0174_tags_on_homepage_watchlist_on_homepage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tags'),
        ),
    ]
