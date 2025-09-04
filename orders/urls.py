from django.urls import path
from orders.views import OrderView

urlpatterns = [
    path("list/", OrderView.as_view()),
]
