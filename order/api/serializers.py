from rest_framework import serializers
from order.models import Wishlist, Basket, BasketItem
from product.api.serializers import VersionListSerializer

class WishlistSerializer(serializers.ModelSerializer):
    items = VersionListSerializer()

    class Meta:
        model = Wishlist
        fields = [
            'user',
            'items'
        ]

class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = [
            'user',
            'items'
        ]

class BasketItemSerializer(serializers.ModelSerializer):
    product = VersionListSerializer()

    class Meta:
        model = BasketItem
        fields = [
            'user',
            'product', 
            'quantity'
        ]