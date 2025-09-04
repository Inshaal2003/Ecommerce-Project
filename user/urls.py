from django.urls import path
from user.views import UserLoginAPI, UserLogoutAPI, UserRegisterAPI

urlpatterns = [
    path("login/", UserLoginAPI.as_view()),
    path("register/", UserRegisterAPI.as_view()),
    path("logout/", UserLogoutAPI.as_view()),
]
