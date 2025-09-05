from django.db import models
from user.models import User


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Company Model
class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Prdouct Model
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    @property
    def in_stock(self):
        return self.stock > 0

    # Magic Method
    def __str__(self):
        return f"{self.title} has a price of {self.price}."


# Reviews Model
class Reviews(models.Model):
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    # Foreign Key
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Magic Method
    def __str__(self) -> str:
        return f"{self.product.title} has a rating of {self.rating}"
