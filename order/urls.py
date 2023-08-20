from django.urls import path
from .views import CartView, WishlistView, CartVerifyView, card, card_verify

urlpatterns = [
    path('cart/', CartView.as_view(), name = "cart"),
    path('cart_verify/', CartVerifyView.as_view(), name = "cart_verify"),
    path('card/', card, name = "card"),
    path('card_verify/', card_verify, name = "card_verify"),
    path('wishlist/', WishlistView.as_view(), name="wishlist")
]