from django.utils import timezone
from django.db import models
from users.models import Users
from admin_actions.models import Admin
from media.models import Media
import string
import random

def generate_short_uuid(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_unique_product_id():
    while True:
        new_id = generate_short_uuid()
        if not Product.objects.filter(product_id=new_id).exists():
            return new_id

def generate_unique_payment_id():
    while True:
        new_id = generate_short_uuid()
        if not Payment.objects.filter(payment_id=new_id).exists():
            return new_id

def products_image_upload_path(instance, filename):
    return f'products/{filename}'


class Product(models.Model):
    product_id = models.CharField(max_length=10, default=generate_unique_product_id, editable=False, primary_key=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')

    def __str__(self):
        return f"Product {self.product_id}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=products_image_upload_path)

    def __str__(self):
        return f"Image for {self.product.title}"


class Payment(models.Model):
    payment_id = models.CharField(max_length=10, default=generate_unique_payment_id, primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount}"


class Cart(models.Model):
    cart_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.user and not self.cart_id:
            self.cart_id = str(self.user.user_id)[:10]  # truncate if longer than 10 chars
        super().save(*args, **kwargs)

    def update_total(self):
        self.total_amount = sum(item.line_total for item in self.items.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_id')
    count = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.line_total = self.product.price * self.count
        super().save(*args, **kwargs)
        self.cart.update_total()
