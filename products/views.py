from decimal import Decimal
from urllib import request
import uuid
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
import hashlib
import os
from django.shortcuts import get_object_or_404

from order.models import Order, OrderItem
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

#list all products for admins
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_products(request):
    if not request.user.is_staff:
        return Response({'error': 'User is not an admin.'}, status=status.HTTP_403_FORBIDDEN)   
    
    data = request.data.copy()
    data['admin_id'] = request.user.user_id
    data['user_id'] = request.user.user_id

    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = serializer.save()
        return Response({
            'success': True,
            'message': 'Product created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# Delete a product (admin only)
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_product(request, product_id):
    product = Product.objects.filter(product_id=product_id).first()
    if not product:
        return Response({
            'success': False,
            'message': 'Product not found',
        }, status=status.HTTP_404_NOT_FOUND)
    
    if product.image and product.image.name:
        if os.path.isfile(product.image.path):
            os.remove(product.image.path)
    
    product.delete()
    return Response({
        'success': True,
        'message': 'Product and its image deleted successfully',
    }, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAdminUser])
def update_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    partial = request.method == 'PATCH'
    data = request.data.copy()
    data['admin_id'] = request.user.user_id
    if 'product_id' in data:
        data.pop('product_id')


    serializer = ProductSerializer(product, data=data, partial=partial)

    if serializer.is_valid():
        updated_product = serializer.save()
        response_serializer = ProductSerializer(updated_product)
        return Response({
            'success': True,
            'message': 'Product updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


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

    order_id = str(uuid.uuid4())[0:20]
    amount = "{:.2f}".format(float(request.data.get("total_amount", 0)))
    currency = "LKR"

    items_list = request.data.get("items", [])
    items = ", ".join([str(item["product_id"]) for item in items_list]) if items_list else "Products"

    return_url = "http://localhost:5173/user"
    cancel_url = "http://localhost:3000/news"
    notify_url = "http://localhost:8000/api/products/payment/payment_notify"
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
def product_detail(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
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

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # PayHere does not send auth token
def payment_notify(request):
    merchant_id = "1231902"
    merchant_secret = "OTgwNzgzMzI3MzM5Njc5MTc4NzIyMTg4NTYwNTI3ODYyMzc0MDU="

    print("🔥 Payment notify called")
    print("POST DATA:", request.POST)





@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_payment(request):
    try:
        user = request.user
        data = request.data
        product_id = data.get("product_id")
        amount = Decimal(data.get("amount"))
        payment_id = data.get("payment_id")  # you can generate a temporary id

        product = Product.objects.get(product_id=product_id)
        

        payment = Payment.objects.create(
            payment_id=payment_id,
            product_id=product,
            user_id=user,
            amount=amount,
            date_time=timezone.now()
        )
        
        # 2️⃣ Create Order
        order_id = uuid.uuid4().hex[:20]  # limit to 20 chars
        order = Order.objects.create(
            order_id=order_id,
            payment_id=payment,
            price=amount
        )

        # 3️⃣ Create OrderItems
        items = data.get("items", [])  # list of products with quantity
        print(items)
        for item in items:
            product = Product.objects.get(product_id=item["product_id"])
            quantity = item.get("quantity", 1)
            OrderItem.objects.create(
                order_id=order,
                product_id=product,
                quantity=quantity
            )

        return JsonResponse({
            "success": True,
            "payment_id":payment_id,
            "order_id": order.order_id
        })
    except Exception as e:
        print("Error saving payment:", e)
        return JsonResponse({"success": False, "error": str(e)}, status=500)
