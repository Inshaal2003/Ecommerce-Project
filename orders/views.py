from rest_framework.response import Response
from rest_framework.views import APIView, status

from .models import Order
from .serializers import OrderSerializer


# Order List View
class OrderView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        order_query_set = Order.objects.all()
        serialize_query_set = self.serializer_class(order_query_set, many=True)
        return Response(serialize_query_set.data)

    def post(self, request):
        serialize_query_set = self.serializer_class(data=request.data)
        if serialize_query_set.is_valid():
            serialize_query_set.save()
            return Response(serialize_query_set.data, status=status.HTTP_201_CREATED)
        return Response(serialize_query_set.errors, status=status.HTTP_400_BAD_REQUEST)
