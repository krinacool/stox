# Generated by Django 4.2.5 on 2023-11-04 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0081_default_watchlist_alter_customuser_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='access_token',
            field=models.UUIDField(default='4b29d70401b64aeca5f27e5fd2c18256', unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='remark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.remarks'),
        ),
    ]
