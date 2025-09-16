from rest_framework import serializers
from .models import Order, OrderItem


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
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Order
        fields = ["username", "order_id", "order_items", "status", "created_at"]
        extra_kwargs = {
            "order_id": {"read_only": True},
            "created_at": {"read_only": True},
            "status": {"read_only": True},
        }


class OrderStatusSerializer(serializers.ModelSerializer):
    """This is for changing the status from Pending to Confirmed to Completed."""

    class Meta:
        model = Order
        fields = ["status"]


class OrderCancelSerializer(serializers.ModelSerializer):
    """This is for changing the status from Pending to Cancelled."""

    class Meta:
        model = Order
        fields = ["status"]


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        product_id = serializers.IntegerField(source="product.id")

        class Meta:
            model = OrderItem
            fields = ["product_id", "quantity"]

        def validate_quantity(self, value):
            if value == 0:
                raise serializers.ValidationError(
                    "You can not enter 0 as a quantity. Genius"
                )
            return value

    order_data = OrderItemCreateSerializer()

    class Meta:
        model = Order
        fields = ["order_data"]

    def create(self, validated_data):
        product = validated_data.pop("product")
        user = validated_data.pop("user")
        quantity = validated_data.pop("quantity")

        if quantity > product.stock:
            raise serializers.ValidationError(
                "We do not have enough stock to match your order."
            )

        product.stock = product.stock - quantity
        product.save()

        order = Order.objects.create(user=user)
        order_items = OrderItem.objects.create(
            order=order, product=product, quantity=quantity
        )
        return order
