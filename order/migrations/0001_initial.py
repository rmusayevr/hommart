# Generated by Django 4.1.9 on 2023-06-09 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Basket',
                'verbose_name_plural': 'Baskets',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(related_name='products_wishlist', to='product.productversion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.TextField(blank=True, null=True)),
                ('address_link', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('cash', 'cash'), ('cart', 'cart'), ('online', 'online')], max_length=50)),
                ('basket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to='order.basket')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_basket_item', to='product.productversion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_basket_item', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Basket Item',
                'verbose_name_plural': 'Basket Items',
            },
        ),
        migrations.AddField(
            model_name='basket',
            name='items',
            field=models.ManyToManyField(related_name='basket_items', to='order.basketitem'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_basket', to=settings.AUTH_USER_MODEL),
        ),
    ]
