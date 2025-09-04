from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from user.models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework.views import APIView, status

# from rest_framework.permissions import AllowAny, IsAdminUser


class UserLoginAPI(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            username = serialized_data.validated_data.get("username")
            password = serialized_data.validated_data.get("password")
            userObj = authenticate(username=username, password=password)
            login(request, userObj)
            return Response({"message": "Login Sucessfull."})
        return Response(
            {"message": "Login Unsucessfull"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserRegisterAPI(APIView):
    serializer_class = UserRegisterSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request):
        query_set = User.objects.all()
        serialized_query_set = self.serializer_class(query_set, many=True)
        return Response(serialized_query_set.data)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            username = serialized_data.validated_data.get("username")
            password = serialized_data.validated_data.get("password")
            userObj = authenticate(username=username, password=password)
            login(request, userObj)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout Sucessfull."}, status=status.HTTP_200_OK)
