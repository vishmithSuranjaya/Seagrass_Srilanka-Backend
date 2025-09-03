from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import News
from .serializers import NewsSerializer, NewsCreateSerializer

#for google calender functions
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os


# Reading all published news articles
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def read_news(request):
    news = News.objects.filter(is_published=True).order_by('-created_at')
    serializer = NewsSerializer(news, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })

# Get single news article by ID
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_news_detail(request, news_id):
    news = get_object_or_404(News, news_id=news_id, is_published=True)
    serializer = NewsSerializer(news)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_news(request):
    serializer = NewsCreateSerializer(data=request.data)
    if serializer.is_valid():
        news = serializer.save()
        response_serializer = NewsSerializer(news)
        return Response({
            'success': True,
            'message': 'News article created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# Update existing news article
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAdminUser])
def update_news(request, news_id):
    news = get_object_or_404(News, news_id=news_id)
    
    # Use partial update for PATCH requests
    partial = request.method == 'PATCH'
    serializer = NewsCreateSerializer(news, data=request.data, partial=partial)
    
    if serializer.is_valid():
        updated_news = serializer.save()
        response_serializer = NewsSerializer(updated_news)
        return Response({
            'success': True,
            'message': 'News article updated successfully',
            'data': response_serializer.data
        })
    
    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# Delete news article
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_news(request, news_id):
    news = get_object_or_404(News, news_id=news_id)
    news.delete()
    return Response({
        'success': True,
        'message': 'News article deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)

# Get all news for admin (including unpublished)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_news_list(request):
    news = News.objects.all().order_by('-created_at')
    serializer = NewsSerializer(news, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })


#for google calender functions
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # allow http for local dev

# Step 1: Redirect to Google
def google_login(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar.readonly"]
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    request.session["state"] = state
    return HttpResponseRedirect(authorization_url)

# Step 2: Handle Google callback
def google_callback(request):
    state = request.session["state"]
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar.readonly"],
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Save tokens in session (or DB)
    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }

    return HttpResponseRedirect("http://localhost:3000/calendar")  # redirect React frontend

# Step 3: Fetch calendar events
def get_calendar_events(request):
    events = News.objects.all().values("news_id", "title", "created_at", "updated_at")
    return JsonResponse(list(events), safe=False)