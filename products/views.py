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
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get(self, request):
        queryset = Product.objects.all()
        serialized_data = self.serializer_class(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPI(APIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(queryset)
        return Response(serialized_data.data)

    def put(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(queryset, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serialized_data = self.serializer_class(
            queryset, data=request.data, partial=True
        )
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
