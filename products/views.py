from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser


class ProudctListAPI(APIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Anyone can view the product due to self.permission_classes = [AllowAny]"""
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            """Only Admins can add products due to IsAdminUser class"""
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get(self, request):
        """Viewing all the products."""
        queryset = Product.objects.all()
        serialized_data = self.serializer_class(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Adding a product to the database."""
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPI(APIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Only admins can update and delete a product."""
        self.permission_classes = [IsAdminUser]
        if self.request.method == "GET":
            """Anyone can only view the product."""
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, pk):
        """Viewing a product."""
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(queryset)
        return Response(serialized_data.data)

    def put(self, request, pk):
        """Updating a product"""
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(queryset, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Updaing a single field in a product"""
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(
            queryset, data=request.data, partial=True
        )
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Deleting a product"""
        queryset = get_object_or_404(Product, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
