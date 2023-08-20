from rest_framework import serializers
from product.models import Product, Category, ProductVersion, Brand, Image


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'slug'
        )


class CategoryListSerializer(serializers.ModelSerializer):
    parent = SubCategoryListSerializer()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'parent',
            'slug'
        )


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'slug'
        )


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image'
        ]


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = [
            'id',
            'slug'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    brand = BrandListSerializer()
    version = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    twelve_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'brand',
            'price',
            'in_sale',
            'final_price',
            'detail_url',
            'version',
            'image',
            'twelve_price',
        ]

    def get_version(self, obj):
        return obj.get_product_version.pk

    def get_detail_url(self, obj):
        return obj.get_absolute_url()
    
    def get_image(self, obj):
        return obj.get_product_version.image.first().image.url
    
    def get_twelve_price(self, obj):
        if obj.in_sale:
            return round((obj.final_price / 12), 3)
        return round((obj.price / 12), 2)


class VersionListSerializer(serializers.ModelSerializer):
    image = ImageListSerializer(many=True)
    product = ProductListSerializer()

    class Meta:
        model = ProductVersion
        fields = [
            'id',
            'image',
            'slug',
            'product'
        ]
