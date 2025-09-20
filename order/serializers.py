from rest_framework import serializers
from order.models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product(self, obj):
        from products.models import Product
        try:
            prod = Product.objects.get(product_id=obj.product_id)
            from products.serializers import ProductSerializer
            return ProductSerializer(prod).data
        except Product.DoesNotExist:
            return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"