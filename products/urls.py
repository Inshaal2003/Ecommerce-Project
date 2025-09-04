from django.urls import path

from products.views import ProudctAPI

urlpatterns = [path("list/", ProudctAPI.as_view())]
