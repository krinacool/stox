# Generated by Django 4.2.5 on 2024-06-27 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0139_watchlist_is_default_alter_customuser_access_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='lot_size',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='lot_size',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='7b9a9452eea743e1a0e7e2b776067b3c', unique=True),
        ),
    ]
