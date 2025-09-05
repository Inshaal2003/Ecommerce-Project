from django.db import models
from user.models import User
from products.models import Product
import uuid


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"
        COMPLETED = "Completed"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product,
        through="OrderItem",
    )

    # Magic methods
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()

    # Foreign Keys
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    # Magic methods
    def __str__(self):
        return f"{self.quantity} x {self.product.title} in order {self.order.order_id}"
