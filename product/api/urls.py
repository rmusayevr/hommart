from django.urls import path
from .views import VersionListAPIView, ProductListAPIView

urlpatterns = [
    path('api/versions/', VersionListAPIView.as_view(), name = "versions"),
    path('api/products/', ProductListAPIView.as_view(), name = "api-products")
]
