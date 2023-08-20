from django.urls import path
from .views import HomePage, SearchView, ErrorView

urlpatterns = [
    path('', HomePage.as_view(), name = "home"),
    path('search/', SearchView, name="search"),
    path('error/', ErrorView, name="error"),
    
]