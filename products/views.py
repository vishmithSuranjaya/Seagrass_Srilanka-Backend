from urllib import request
import uuid
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
import hashlib

from users.models import Users
from .models import Product, Cart, Payment, CartItem
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


# #add a product to user's cart
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def add_to_cart(request):
#     serializer = CartSerializer(data = request.data)
#     if serializer.is_valid():
#         serializer.save(user_id= request.user)
#         return Response(serializer.data, status= status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

#view for the payment gatway
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_payment(request):
    merchant_id = "1231902"
    merchant_secret = "OTgwNzgzMzI3MzM5Njc5MTc4NzIyMTg4NTYwNTI3ODYyMzc0MDU="

    order_id = str(uuid.uuid4())
    amount = "{:.2f}".format(float(request.data.get("total_amount", 0)))
    currency = "LKR"

    items_list = request.data.get("items", [])
    items = ", ".join([str(item["product_id"]) for item in items_list]) if items_list else "Products"

    return_url = "http://localhost:5173/user"
    cancel_url = "http://localhost:3000/news"
    notify_url = "http://localhost:8000/api/products/payment/payment_notify/"
    secret_hash = hashlib.md5(merchant_secret.encode('utf-8')).hexdigest().upper()

    hash_string = merchant_id + order_id + amount + currency + secret_hash

    hash_value = hashlib.md5(hash_string.encode('utf-8')).hexdigest().upper()
    # --------------------------

    payload = {
        "sandbox": True,
        "merchant_id": merchant_id,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "notify_url": notify_url,
        "order_id": order_id,
        "items": items,
        "amount": amount,
        "currency": currency,
        "hash": hash_value,
        "first_name": "Seagrass",
        "last_name": "Sri Lanka",
        "email": "suranjaya0327@gmail.com",
        "phone": "0771234567",
        "address": "Colombo",
        "city": "Colombo",
        "country": "Sri Lanka",
    }

    return JsonResponse(payload)


#display a product when the id is given
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data)

#get products in the cart
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) 
def get_user_cart(request):
    try:
        # Prefetch items to include CartItems
        cart = Cart.objects.prefetch_related('items').get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart is empty."}, status=200)
    

#view for the add items to the cart
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get("product_id")
    count = int(request.data.get("count", 1))

    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # Create or get Cart for this user
    cart, created = Cart.objects.get_or_create(
        user=user,
        defaults={"total_amount": 0, "cart_id": str(user.user_id)}  # cart_id same as user_id
    )

    # Create or update CartItem
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,       # pass the Cart instance
        product=product, # link to product instance
        defaults={"count": count}
    )

    if not item_created:
        cart_item.count += count
    cart_item.save()  # this updates line_total and cart.update_total()

    return Response({
        "message": "Item added to cart",
        "cart_id": cart.cart_id,
        "product": product.product_id,
        "count": cart_item.count,
        "line_total": cart_item.line_total,
        "total_cart_amount": cart.total_amount
    }, status=201)

#to update the cart item count
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product__product_id=product_id)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({"error": "Item not found in cart."}, status=404)

    count = int(request.data.get("count", cart_item.count))
    if count < 1:
        return Response({"error": "Count must be at least 1."}, status=400)

    cart_item.count = count
    cart_item.save()  # automatically updates line_total and cart total
    return Response({
        "message": "Cart item updated.",
        "product": cart_item.product.product_id,
        "count": cart_item.count,
        "line_total": cart_item.line_total,
        "total_cart_amount": cart.total_amount
    }, status=200)

#remove items form the cart
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_cart_item(request, product_id):
    """
    Remove a specific product from the logged-in user's cart.
    """
    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)

        # Find the cart item for this product
        cart_item = CartItem.objects.get(cart=cart, product__product_id=product_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

    # Delete the cart item
    cart_item.delete()

    # Cart total will auto-update if using CartItem.save() for updates, 
    # otherwise update manually
    cart.update_total()

    return Response({
        "message": "Item removed from cart.",
        "total_cart_amount": cart.total_amount
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # PayHere does not send auth token
def payment_notify(request):
    merchant_id = "1231902"
    merchant_secret = "OTgwNzgzMzI3MzM5Njc5MTc4NzIyMTg4NTYwNTI3ODYyMzc0MDU="
    # --- Step 1: Extract required data ---
    data = request.POST  # PayHere sends data as form-encoded
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")
    amount = data.get("amount")
    currency = data.get("currency")
    received_hash = data.get("hash")
    status_code = data.get("status_code")  # 2 = success, 3 = failed, 0 = pending
    customer_email = data.get("email")
    product_name = data.get("items")  # the product name(s) sent in payment creation

    # --- Step 2: Verify hash ---
    hash_string = merchant_id + order_id + str(amount) + currency + merchant_secret
    expected_hash = hashlib.md5(hash_string.encode('utf-8')).hexdigest().upper()

    if received_hash != expected_hash:
        # Invalid request, ignore or log
        return Response("Invalid hash", status=400)

    # --- Step 3: Process only successful payments ---
    if status_code == "2":  # Payment success
        # Find user by email
        try:
            user = Users.objects.get(email=customer_email)
        except Users.DoesNotExist:
            return Response("User not found", status=404)

        # Find product by name (or handle multiple products)
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response("Product not found", status=404)

        # Create Payment record
        Payment.objects.create(
            payment_id=payment_id,
            product_id=product,
            user_id=user,
            amount=amount,
            date_time=timezone.now(),
        )

        # Optionally, clear cart items for this user
        user.cart.items.all().delete()
    
    # --- Step 4: Respond to PayHere ---
    return Response("OK", status=200)