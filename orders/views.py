from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from products.models import Product
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderCancelSerializer, OrderSerializer, OrderStatusSerializer


# Order List View
class OrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Only Logged in users can view their orders."""
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please login to view your orders"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        """Filter the orders according to the users"""
        order_query_set = Order.objects.filter(user=request.user)
        """Check if user is admin so that he can view all products."""
        if request.user.is_staff:
            order_query_set = Order.objects.all()
        serialize_query_set = self.serializer_class(order_query_set, many=True)
        return Response(serialize_query_set.data)


class OrderDetailView(APIView):
    def get_permissions(self):
        """Only Admins can update and delete orders."""
        self.permission_classes = [IsAdminUser]
        if self.request.method == "GET":
            """User has to login to view their orders."""
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please login to view your orders."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_query = get_object_or_404(Order, pk=pk)
        serialize_query_set = OrderSerializer(order_query)
        return Response(serialize_query_set.data)

    def patch(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"message": "Sorry You are not allowed to perform this operation."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_query = get_object_or_404(Order, pk=pk)
        serialize_query_set = OrderStatusSerializer(
            order_query, data=request.data, partial=True
        )
        if serialize_query_set.is_valid():
            serialize_query_set.save()
            return Response(serialize_query_set.data)
        return Response(serialize_query_set.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelView(APIView):
    serializer_class = OrderCancelSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please login to cancel your order."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_query = get_object_or_404(Order, pk=pk)
        serialize_query_set = self.serializer_class(
            order_query, data=request.data, partial=True
        )
        if serialize_query_set.is_valid():
            serialize_query_set.save()
            return Response(
                {"message": "Your order has been cancelled."}, status=status.HTTP_200_OK
            )
        return Response(serialize_query_set.errors, status=status.HTTP_400_BAD_REQUEST)


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
            if quantity > product.stock:
                return Response(
                    {
                        "message": f"We don't have enough stock to complete your order. Only {product.stock} items are available right now."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            product.stock = product.stock - quantity
            product.save()
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
