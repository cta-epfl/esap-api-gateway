# Generated by Django 3.1.4 on 2021-12-07 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0002_auto_20200821_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='equinox',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='protocol',
        ),
        migrations.AddField(
            model_name='dataset',
            name='visibility',
            field=models.CharField(default='archive', max_length=100),
        ),
    ]
