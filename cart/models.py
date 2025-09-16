from django.db import models
from user.models import User
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
