# Generated by Django 2.1.2 on 2019-01-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0024_auto_20190101_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='jmb_bg1',
            field=models.CharField(default='#505050', max_length=8),
        ),
        migrations.AddField(
            model_name='season',
            name='jmb_bg2',
            field=models.CharField(default='#202020', max_length=8),
        ),
        migrations.AddField(
            model_name='season',
            name='jmb_col',
            field=models.CharField(default='#ffffff', max_length=8),
        ),
    ]
