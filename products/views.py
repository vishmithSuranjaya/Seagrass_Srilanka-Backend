from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Product, Cart, Payment
from .serializers import ProductSerializer, CartSerializer, PaymentSerializer

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

