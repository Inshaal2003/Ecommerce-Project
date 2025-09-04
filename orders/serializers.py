from rest_framework import serializers
from .models import Order, OrderItem


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
