# Generated by Django 3.2 on 2023-08-20 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_watchlist_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together={('user', 'stock')},
        ),
    ]
