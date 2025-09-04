from django.urls import path
from orders.views import OrderCreateView, OrderView

urlpatterns = [
    path("order-list/", OrderView.as_view()),
    path("create-orders/", OrderCreateView.as_view()),
]
