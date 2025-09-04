from django.urls import path

from products.views import ProudctListAPI, ProductDetailAPI

urlpatterns = [
    path("product-list/", ProudctListAPI.as_view()),
    path("product-detail/<int:pk>", ProductDetailAPI.as_view()),
]
