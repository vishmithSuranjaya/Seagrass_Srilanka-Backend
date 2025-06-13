from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Blog, Comments
from .serializers import BlogSerializer, CommentSerializer

#listing all the blogs
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_list(request):
    blogs = Blog.objects.all
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

#registered user posts a new blog
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(date=timezone.now(), time=timezone.now().time())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        data['blog_id'] = parent_comment.blog_id
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
def blog_reading(request , blog_id):
    try:
        blog = Blog.objects.get(blog_id = blog_id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not Found"} , status = status.HTTP_404_NOT_FOUND)
 
