from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions,status
from order.models import Order
from order.serializers import OrderSerializer
from products.models import Payment
from products.serializers import PaymentSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_orders(request):
    # Step 1: Get all payments made by this user
    payments = Payment.objects.filter(user_id=request.user.user_id)

    # Step 2: Serialize including related orders and order items
    serializer = PaymentSerializer(payments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def admin_list_orders(request):
    orders = Order.objects.prefetch_related('items__product_id').all().order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def admin_update_order_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    if status_value is not None:
        order.status = bool(status_value)
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'message': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)