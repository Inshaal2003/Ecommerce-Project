from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from user.models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework.views import APIView, status

# from rest_framework.permissions import AllowAny, IsAdminUser


class UserLoginAPI(APIView):
    # Defining the serializer class.
    serializer_class = UserLoginSerializer
    # Allowing anyone to send a login request.
    permission_classes = [AllowAny]

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            username = serialized_data.validated_data.get("username")  # pyright: ignore
            password = serialized_data.validated_data.get("password")  # pyright: ignore
            userObj = authenticate(username=username, password=password)
            login(request, userObj)
            return Response({"message": "Login Sucessfull."})
        return Response(
            {"message": "Login Unsucessfull"}, status=status.HTTP_400_BAD_REQUEST
        )


""" URL: http://127.0.0.1:8000/api/account/register/ """


class UserRegisterAPI(APIView):
    """Specifying the User Serializer Class."""

    serializer_class = UserRegisterSerializer

    """Specifying the permissions."""

    def get_permissions(self):
        """If method is Post allow anyone to access the api."""
        self.permission_classes = [AllowAny]
        """Only admins are allowed to get access to api that shows all users."""
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    """get method for displaying all the users."""

    def get(self, request):
        query_set = User.objects.all()
        serialized_query_set = self.serializer_class(query_set, many=True)
        return Response(serialized_query_set.data)

    """post method for registering a user."""

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            """Saving the user data into db and returning the user."""
            userObj = serialized_data.save()
            """
            Popping out the user password and username and than passing them into to the authenticate method 
            which will authenticate the user and return the user object.

            password = serialized_data.validated_data.get("password")  # pyright: ignore
            username = serialized_data.validated_data.get("username")  # pyright: ignore
            userObj = authenticate(username=username, password=password)

            There is no need to do this since serialized_data.save() is returning the user.
            """
            login(request, userObj)  # pyright: ignore
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout Sucessfull."}, status=status.HTTP_200_OK)
