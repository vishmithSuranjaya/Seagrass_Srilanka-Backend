from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Product, Cart, Payment
from .serializers import ProductSerializer, CartSerializer, PaymentSerializer
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


#list all products
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)

#new product is added by the admin
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_products(request):
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#add a product to user's cart
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    serializer = CartSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(user_id= request.user)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#this is for buying the products in the cart . used in checkout process
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def buy_products(request):
    cart_items = Cart.objects.filter(user_id=request.user)
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CartSerializer(cart_items, many=True)
    return Response({"message": "Buy products initiated", "cart": serializer.data}, status=status.HTTP_200_OK)


#process and save payments of a product
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id = request.user, date_time = timezone.now())
        Cart.objects.filter(user_id=request.user).delete()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def create_payment(request):
    merchant_id = "YOUR_MERCHANT_ID"
    merchant_secret = "YOUR_MERCHANT_SECRET"

    order_id = "ORDER1234"
    amount = "1000.00"
    currency = "LKR"

    return_url = "http://localhost:3000/payment-success"
    cancel_url = "http://localhost:3000/payment-cancel"
    notify_url = "http://127.0.0.1:8000/api/payment/notify/"  # backend callback

    # Generate hash (MD5 uppercase)
    hash_string = merchant_id + order_id + amount + currency + merchant_secret
    hash_value = hashlib.md5(hash_string.encode('utf-8')).hexdigest().upper()

    payload = {
        "sandbox": True,
        "merchant_id": merchant_id,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "notify_url": notify_url,
        "order_id": order_id,
        "items": "Test Item",
        "amount": amount,
        "currency": currency,
        "hash": hash_value,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "0771234567",
        "address": "Colombo",
        "city": "Colombo",
        "country": "Sri Lanka",
    }

    return JsonResponse(payload)


