# Generated by Django 5.0.3 on 2024-09-16 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_ca_link_news_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExploreVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Explore Video',
                'verbose_name_plural': 'Explore Videos',
            },
        ),
    ]
