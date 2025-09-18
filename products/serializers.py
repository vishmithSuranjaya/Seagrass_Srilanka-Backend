from rest_framework import serializers
from .models import Product, Cart, Payment, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Description cannot exceed 200 characters.")
        return value.strip()

    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError("Price is required.")
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
  

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ='__all__'

# class CartItemSerializer(serializers.ModelSerializer):
#     # class Meta:
#     #     model = CartItem
#     #     fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.product_id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=20, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_name", "product_price", "product_image", "count", "line_total"]

        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'