# Generated by Django 4.1.9 on 2023-06-09 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'cash'), ('online', 'online'), ('cart', 'cart')], max_length=50),
        ),
    ]