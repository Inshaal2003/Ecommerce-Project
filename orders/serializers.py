from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.title")
    produt_category = serializers.CharField(source="product.category")
    # product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product_name", "produt_category", "quantity", "item_subtotal"]
        # fields = ["product", "quantity", "item_subtotal"]


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["order_id", "order_items", "status", "created_at"]
        extra_kwargs = {
            "order_id": {"read_only": True},
            "created_at": {"read_only": True},
            "status": {"read_only": True},
        }
