from rest_framework import serializers
from .models import Product, Cart, Payment, CartItem, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)  

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
    orders = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields ='__all__'

    def get_orders(self, obj):
        # lazy import to prevent circular import
        from order.serializers import OrderSerializer
        # assumes related_name='orders' in Order.payment FK
        orders = obj.orders.all()
        return OrderSerializer(orders, many=True).data
# class CartItemSerializer(serializers.ModelSerializer):
#     # class Meta:
#     #     model = CartItem
#     #     fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.product_id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=20, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'

    def get_product_image(self, obj):
        first_image = obj.product.images.first()  # <-- use related_name "images"
        if first_image:
            return first_image.image.url
        return None
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'