# Generated by Django 5.0.3 on 2024-07-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0147_alter_customuser_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='6e06a88e2d044e25ac18a19eba1db994', unique=True),
        ),
    ]
