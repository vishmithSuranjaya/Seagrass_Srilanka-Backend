from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Research_articles
from .serializers import ResearchArticleSerializer


#list all research articles
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def research_article_list(request):
    articles = Research_articles.objects.all()
    serializer = ResearchArticleSerializer(articles, many = True)
    return Response(serializer.data)

#admin adding some research article to the website
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_research_articles(request):
    serializer = ResearchArticleSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.http_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)