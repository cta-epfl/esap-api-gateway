# Generated by Django 4.0.3 on 2022-05-07 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facility',
            options={'ordering': ['facilitytype', 'name']},
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
    ]
