from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from products.models import Product
from news.models import News
from research.models import Research_articles
from media.models import Media
from .serializers import AdminSerializer
from products.serializers import ProductSerializer
from news.serializers import NewsSerializer
from research.serializers import ResearchArticleSerializer
from .models import Admin
from media.serializers import MediaSerializer
from blogs.models import Blog

#admin adding a new product
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_products(request):
    serializer = ProductSerializer(data=request.data)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#admin adding news 
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_news(request):
    serializer = NewsSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save(date=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#admin adding a research article
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_research_articles(request):
    serializer = ResearchArticleSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#admin managing the gallery
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def manage_gallery(request):
    if request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        media = Media.objects.create(
            media_id=f"media_{timezone.now().strftime('%Y%m%d_%H%M%S')}",
            name=file.name,
            link=file_name,
            type=file.content_type,
            admin_id=Admin.objects.first()  
        )
        serializer = MediaSerializer(media) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)


#admin deleting content like products, news, research articles, media etc
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_content(request, model_name, id_value):
    model_map = {
        'blog' : Blog,
        'product': Product,
        'news': News,
        'research_article': Research_articles,
        'media': Media
    }
    if model_name.lower() in model_map:
        try:
            instance = model_map[model_name.lower()].objects.get(pk=id_value)
            instance.delete()
            return Response({"message": f"{model_name} deleted"}, status=status.HTTP_200_OK)
        except model_map[model_name.lower()].DoesNotExist:
            return Response({"error": f"{model_name} not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)