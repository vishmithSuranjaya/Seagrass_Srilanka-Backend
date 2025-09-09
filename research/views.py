from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Research_articles
from .serializers import ResearchArticleSerializer, ResearchArticleCreateSerializer
import uuid 

# List all research articles
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def research_article_list(request):
    articles = Research_articles.objects.all()
    serializer = ResearchArticleSerializer(articles, many=True)
    return Response({"data": serializer.data})

# Admin adds new article
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_research_articles(request):
    if not request.user.is_staff:
        return Response({'error': 'User is not an admin.'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data.copy()
    data['admin_id'] = request.user.user_id 

    serializer = ResearchArticleCreateSerializer(data=data)
    if serializer.is_valid():
        article = serializer.save()
        response_serializer = ResearchArticleSerializer(article)
        return Response({
            'success': True,
            'message': 'Research article created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# Admin updates an existing article
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAdminUser])
def update_research_article(request, research_id):
    try:
        article = Research_articles.objects.get(research_id=research_id)
    except Research_articles.DoesNotExist:
        return Response({"message": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['admin_id'] = request.user.user_id  

    serializer = ResearchArticleSerializer(article, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin deletes an article
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_research_article(request, research_id):
    try:
        article = Research_articles.objects.get(research_id=research_id)
    except Research_articles.DoesNotExist:
        return Response({"message": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    article.delete()
    return Response({"message": "Article deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Search for research articles by keyword
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_research_articles(request):
    keyword = request.GET.get('q', '')
    if keyword:
        articles = Research_articles.objects.filter(
            Q(research_id__icontains=keyword) |
            Q(link__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(title__icontains=keyword)
        )
    else:
        articles = Research_articles.objects.all()
    serializer = ResearchArticleSerializer(articles, many=True)
    return Response(serializer.data)
