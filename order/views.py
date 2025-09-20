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