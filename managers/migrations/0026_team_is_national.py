# Generated by Django 2.1.2 on 2019-01-01 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0025_auto_20190101_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_national',
            field=models.BooleanField(default=False),
        ),
    ]
