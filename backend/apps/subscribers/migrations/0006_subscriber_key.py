# Generated by Django 2.1.1 on 2020-03-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0005_auto_20200317_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='key',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
