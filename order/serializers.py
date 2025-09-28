
from rest_framework import serializers
from order.models import Order, OrderItem
from users.models import Users  
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()  # for frontend-friendly nested product info

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product(self, obj):
        product = obj.product_id  # <-- your FK field
        if product:
            # get first image from related ProductImage table
            first_image = product.images.first()  # uses related_name="images" from ProductImage
            return {
                "id": product.product_id,
                "title": product.title,
                "price": float(product.price),
                "image": first_image.image.url if first_image else None,
            }
        return None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'fname', 'lname', 'email', 'image', 'full_name']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(source='payment_id.user_id', read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

