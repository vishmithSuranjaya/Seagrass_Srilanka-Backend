from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import News
from .serializers import NewsSerializer

#reading all news 
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def read_news(request):
    news = News.objects.all().order_by('-date')
    serializer = NewsSerializer(news, many = True)
    return Response(serializer.data)

#admin adds some news to the website
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_news(request):
    serializer = NewsSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(date=timezone.now())
        return Response(serializer.data , status = status.HTTP_201_CREATED)
    return Response(serializer.erros, status = status.HTTP_400_BAD_REQUEST)

