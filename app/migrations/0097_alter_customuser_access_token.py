# Generated by Django 4.2.5 on 2023-12-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0096_alter_customuser_access_token_withdrawn_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='1dec7b6a8df441229566443eae3fb876', unique=True),
        ),
    ]
