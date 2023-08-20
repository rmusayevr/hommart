from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from product.models import Product, ProductVersion
from .serializers import VersionListSerializer, ProductListSerializer
from django_filters import Filter, FilterSet, NumberFilter
from rest_framework.pagination import PageNumberPagination

class VersionListAPIView(ListAPIView):
    queryset = ProductVersion.objects.all()
    serializer_class = VersionListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', )


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class ProductFilter(FilterSet):
    child_category = ListFilter(field_name='category__slug')
    parent_category = ListFilter(field_name='category__parent__slug')
    brand = ListFilter(field_name='brand__slug')
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['child_category', 'parent_category', 'brand', 'min_price', 'max_price']

class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination


