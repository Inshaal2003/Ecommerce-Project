from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from products.models import Product
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import (
    OrderCancelSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


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
    serializer_class = OrderCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            """Popping out proudct_id and quantity."""
            order_data = serializer.validated_data.pop("order_data")
            product_id = order_data["product"]["id"]
            quantity = order_data["quantity"]

            """Checking if there is a product associated with the product id."""
            product = get_object_or_404(Product, pk=product_id)

            """Sending the user obj, product obj and quantity value to the save() method.
            These values will be available in the validated_data dictionary."""
            serializer.save(user=request.user, product=product, quantity=quantity)

            return Response({"message": "Congratulations Your Order has been created."})

        """ If the data is not valid."""
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
