# Generated by Django 4.1.9 on 2023-06-09 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_az',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_ru',
        ),
    ]
