from django.urls import path
from .views import ProductsView, ProductDetailView

urlpatterns = [
    path('products/', ProductsView.as_view(), name="products"),
    path('products/<str:product>/<str:version>/',
         ProductDetailView.as_view(), name="detail")
]
