from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView, status

from products.models import Product

from .models import Order, OrderItem
from .serializers import OrderSerializer


# Order List View
class OrderView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please login to view your orders"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_query_set = Order.objects.filter(user=request.user)
        serialize_query_set = self.serializer_class(order_query_set, many=True)
        return Response(serialize_query_set.data)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": "The product you are trying to buy does not exsist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            order = Order.objects.create(user=request.user)
            orderItem = OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
            return Response(
                {
                    "message": "Your order has been placed your order id is",
                    "order_id": order.order_id,
                },
                status=status.HTTP_201_CREATED,
            )
