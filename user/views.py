from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from user.models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework.views import APIView, status
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework.permissions import AllowAny, IsAdminUser


""" URL: http://127.0.0.1:8000/api/account/login/ """


class UserLoginAPI(APIView):
    # Defining the serializer class.
    serializer_class = UserLoginSerializer
    # Allowing anyone to send a login request.
    permission_classes = [AllowAny]

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            """
            There is no need to this since we are already authenticating user in the serializer class.
            username = serialized_data.validated_data.get("username")  # pyright: ignore
            password = serialized_data.validated_data.get("password")  # pyright: ignore
            userObj = authenticate(username=username, password=password)
            login(request, userObj)
            """
            user = serialized_data.validated_data
            print(user)
            token = RefreshToken.for_user(user)  # pyright: ignore
            return Response(
                {
                    "user": serialized_data.data,
                    "refresh token": str(token),
                    "access token": str(token.access_token),
                }
            )
        return Response(
            {"message": "Login Unsucessfull please provide correct credentials."},
            status=status.HTTP_400_BAD_REQUEST,
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
            self.permission_classes = [IsAdminUser]
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
            token = RefreshToken.for_user(userObj)  # pyright: ignore
            """
            There is no need to use login method. Becuase using login method will create the session.
            login(request, userObj)
            """
            return Response(
                {
                    "user": serialized_data.data,
                    "refresh": str(token),
                    "access": str(token.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


""" URL: http://127.0.0.1:8000/api/account/logout/ """


class UserLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "You have been logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except:
            """
            This is only if you are using session auth.
                logout(request)
            """
            return Response(
                {"message": "Something has gone wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )
