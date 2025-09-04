from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer


class ProudctAPI(APIView):
    serializer_class = ProductSerializer

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
