# Generated by Django 4.2.5 on 2023-11-27 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0089_alter_customuser_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='91ab705b63ad416da393c21872b43046', unique=True),
        ),
    ]
