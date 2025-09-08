from django.contrib import admin
from .models import Product, Cart, Payment

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'price', 'description', 'admin_id')
    list_filter = ('admin_id',)
    search_fields = ('product_id', 'description', 'title')
    fields = ('product_id', 'title', 'image', 'price', 'description', 'admin_id')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'user_id', 'total_amount')
    list_filter = ('user_id',)
    search_fields = ('user_id',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user_id', 'product_id', 'amount', 'date_time')
    list_filter = ('user_id', 'date_time')
    date_hierarchy = 'date_time'
    search_fields = ('payment_id',)