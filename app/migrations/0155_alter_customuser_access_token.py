# Generated by Django 5.0.3 on 2024-07-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0154_alter_shoonya_instrument_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='ee21caceb85548fc9dfd635c385fe18a', unique=True),
        ),
    ]
