from django.db import models

from django.db import models

from products.models import Payment, Product

class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="orders")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} - {self.user.email}"
    

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"