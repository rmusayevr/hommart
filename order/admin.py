from django.contrib import admin
from .models import Wishlist, Basket, BasketItem, Order

admin.site.register(Wishlist)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)
