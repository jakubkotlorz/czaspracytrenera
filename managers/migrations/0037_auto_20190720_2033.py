# Generated by Django 2.1.1 on 2019-07-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0036_auto_20190714_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='teams',
            field=models.ManyToManyField(related_name='seasons', to='managers.Team'),
        ),
    ]
