# Generated by Django 2.1 on 2018-10-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0015_auto_20181014_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externallink',
            name='url',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
