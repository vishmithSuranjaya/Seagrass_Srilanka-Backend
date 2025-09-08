from django.utils import timezone
from django.db import models
from users.models import Users
from admin_actions.models import Admin
from media.models import Media
from django.contrib.auth import get_user_model


def products_image_upload_path(instance, filename):
    return f'products/{filename}'


class Product(models.Model):
    #products model for the merchandise page
    product_id = models.CharField(max_length=20, primary_key = True)
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to=products_image_upload_path, blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField(max_length = 200)
    admin_id =models.ForeignKey(Admin, on_delete= models.CASCADE, to_field='admin_id')

    def __str__(self):
        return f"Product {self.product_id}"
    
# class Cart(models.Model):
#     #cart model
#     cart_id = models.CharField(max_length = 20, primary_key=True)
#     user_id = models.ForeignKey(Users, on_delete =models.CASCADE, to_field='user_id')
#     # product_id = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_id')
#     # count = models.IntegerField(default =1)
#     total_amount = models.DecimalField(max_digits=20, decimal_places = 2,default=1)

#     def __str__(self):
#         return f"Cart {self.cart_id} - {self.user_id}"
    

class Payment(models.Model):
    #this is for payment of products
    payment_id = models.CharField(max_length=20, primary_key = True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    amount = models.DecimalField(max_digits=10, decimal_places = 2)
    date_time = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount}"


    
class Cart(models.Model):
    cart_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Always set cart_id = user_id
        if self.user and not self.cart_id:
            self.cart_id = str(self.user.user_id)
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
