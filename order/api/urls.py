from django.urls import path
from .views import WishlistAPIView, BasketAPIView

urlpatterns = [
    path('api/basket/', BasketAPIView.as_view(), name='api-basket'),
    path('api/wishlist/', WishlistAPIView.as_view(), name = "wishlists"),
]