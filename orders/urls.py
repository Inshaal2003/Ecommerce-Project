from django.urls import path
from orders.views import (
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderView,
)

urlpatterns = [
    path("order-list/", OrderView.as_view()),
    path("create-orders/", OrderCreateView.as_view()),
    path("order-details/<uuid:pk>/", OrderDetailView.as_view()),
    path("cancel-order/<uuid:pk>/", OrderCancelView.as_view()),
]
