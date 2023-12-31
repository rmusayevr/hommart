# Generated by Django 4.1.9 on 2023-06-09 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_category_parent_az_remove_category_parent_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_az',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='product.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_en',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='product.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='product.category'),
        ),
    ]
