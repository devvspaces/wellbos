# Generated by Django 3.2.6 on 2021-08-12 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20210812_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='models_height',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='product',
            name='models_wearing',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
