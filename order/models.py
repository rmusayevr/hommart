from django.db import models
from product.models import Product, ProductVersion
from account.models import User

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishlist")
    items = models.ManyToManyField(ProductVersion, related_name="products_wishlist")

    def __str__(self):
        return f"{self.user}'s wishlist"

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

class BasketItem(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, null=True, blank=True, related_name="product_basket_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_basket_item")

    def __str__(self):
        return f"{self.user.full_name}'s basket item"
    
    def get_total(self):
        if self.product.product.in_sale:
            total = self.product.product.final_price*self.quantity
        else:
            total = self.product.product.price*self.quantity
        return total

    def get_subtotal(self):
        return self.product.product.price*self.quantity
    
    def get_sale(self):
        return self.get_subtotal() - self.get_total()

    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_basket")
    items = models.ManyToManyField(BasketItem, related_name="basket_items")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.full_name}'s basket"

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"


class Order(models.Model):
    methods = {
        ("online", "online"),
        ("cash", "cash"),
        ("cart", "cart")
    }
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE, related_name="user_order")
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    address_link = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=methods)

    def __str__(self):
        return f"{self.full_name}'s order"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

