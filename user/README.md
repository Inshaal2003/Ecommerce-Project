# User App Models
So we started off by building our very own custom user model. There are three ways to build  a custom user model in django.

1. Use the `django.contrib.auth.models.User` models this comes with most fields that are supposed to be in a user model. It logs in by using the `username` and `password`. But beware you can't add or change the fields in this model.

2. The second method is to use the `django.contrib.auth.models.AbstractUser.` model. It is similar to the `django.contrib.auth.models.User` model but it allows adding fields in the model. But it still log in using the `username` field.

3. To change logging in using the `username` fields you can use the `django.contrib.auth.models.AbstractBaseUser` model. This model gives you full control over your `User` model.
But it requires you to write your own fileds and also write your own `user_manager` for creating `users` and `superusers`.


# Serializers
Now for our users app we have created two serializers one is the `UserLoginSerializer` and the second is the `UserRegistrationSerializer`.

## UserRegistrationSerializer
The `UserRegistrationSerializer` inherits from the `serializers.ModelSerializer`. We are using `serializers.ModelSerializer` because we want to store the user data in the database.

## How to hash the password provided by the user. 
1. After calling `is_valid()` method. 
2. We will call the `save()` method. 
3. The `save()` method will internally call the `create()` method. Which checks for a lot of things and than creates the new object by calling the `Model.object.create(**validated_data)` which will create the object and than it is returned.
4. The **problem** with this approach is that the **user will be created** but his **password will not be hashed**. To **hash** the password we have to override the `create()` method and use `Models.object.create_user(**validated_data)` method to create the user this method will hash the password automatically.

## UserLoginSerializer
The `UserLoginSerializer` inherits from the `serializers.Serializers` class since we don't have to store the username and password in the database we just have to compare them.

# Apis
So for apis we have two different apis.
1. UserLoginAPI
2. UserRegistrationAPI

## 1. UserLoginAPI
So for `UserLoginAPI` we are inheriting from `APIView` Class. Than we are only allowing a post request for this particular API.
After that we will verify the data by calling `is_valid()` method. Now the validated data will be placed in the `validated_data` dict and we can access different values using the `validated_data.get("key")` method.
Than just pass the `username` and `password` to the `authenticate()` method which will return you the user object `if authenticated true` but will return `Anonymous` if the user is not authenticated pass the user object to the `login()` function to login the user.

## 2. UserRegisterAPI
The `UserRegisterAPI` we are inheriting from `APIView` Class. The `UserRegisterAPI` will only accept a `POST` request for registering a user.
After validating the data by calling `serializer.is_valid()` method after that we call the `serializer.save()` method.
The `serializers.validated_data.get("username")` and `serializers.validated_data.get("password")` will give us the `username` and `password`. Pass this `username` and `password` to the `authenticate(username=username, password=password)`.
The `authenticate()` method will return the user if authenticated correctly but will return `Anonymous` if the user does not exsist.
Pass the `user object to the login function` and than the user will be `authenticated.`

## 3. UserLogoutAPI
The `UserLogoutAPI` has a `logout()` method which just accepts the `request` instance.
The `LogoutAPI` must be a `POST` request.
