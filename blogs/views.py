from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import Blog, Comments
from .serializers import BlogSerializer, CommentSerializer
import os
import uuid
from django.conf import settings

#listing all the blogs
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_list(request):
    blogs = Blog.objects.all()  
    serializer = BlogSerializer(blogs, many=True, context={'request': request})
    return Response(serializer.data)

#registered user posts a new blog
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_blog(request):
    data = request.data.copy()
    data['blog_id'] = str(uuid.uuid4())[:10]
    data['user_id'] = request.user.user_id
    data['status'] = data.get('status', 'active')
    
    serializer = BlogSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        blog = serializer.save(date=timezone.now().date(), time=timezone.now().time())
        return Response(BlogSerializer(blog, context={'request': request}).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update blog with image
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_blog(request, blog_id):
    try:
        blog = Blog.objects.get(blog_id=blog_id)
        
        if blog.user_id != request.user and not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if 'image' in request.FILES and blog.image:
            if os.path.isfile(blog.image.path):
                os.remove(blog.image.path)
        
        serializer = BlogSerializer(blog, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_blog = serializer.save()
            return Response(BlogSerializer(updated_blog, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete blog
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_blog(request, blog_id):
    try:
        blog = Blog.objects.get(blog_id=blog_id)
        
        if blog.user_id != request.user and not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        blog.delete()  
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

#creating a new comment on the blog
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#replying to an existing comment
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reply_to_comment(request, comment_id):
    try:
        parent_comment = Comments.objects.get(comment_id=comment_id)
        data = request.data.copy()
        data['blog_id'] = parent_comment.blog_id.blog_id  
        data['user_id'] = request.user.user_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Comments.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
   
   
#liking a blog post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_blog(request, blog_id):
    try:
        blog = Blog.objects.get(blog_id=blog_id)
        blog.like_count += 1
        blog.status = f"liked_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
        blog.save()

        return Response({"message": "Blog Liked", "blog_id": blog_id, "like_count": blog.like_count}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)


#Viewing a specific blog post when reading it 
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_reading(request, blog_id):
    try:
        blog = Blog.objects.get(blog_id=blog_id)
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not Found"}, status=status.HTTP_404_NOT_FOUND)