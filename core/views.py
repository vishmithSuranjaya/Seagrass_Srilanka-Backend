from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Gallery_images
from .serializers import GalleryImageSerializer, GalleryImageUpdateSerializer
from admin_actions.models import Admin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid

#getting all the images
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_images(request):
    try:
        images = Gallery_images.objects.all().order_by('-uploaded_at')
        serializer = GalleryImageSerializer(images, many=True)
        return Response({
            "message": "Gallery images retrieved successfully",
            "data": serializer.data,
            "count": images.count()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "error": "Failed to retrieve gallery images",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_gallery_image(request):
    data = request.data.copy()
    
    data['admin_id'] = request.user.user_id  # link to logged-in admin

    serializer = GalleryImageSerializer(data=data)
    if serializer.is_valid():
        image = serializer.save()
        response_serializer = GalleryImageSerializer(image)
        return Response({
            'success': True,
            'message': 'Image uploaded successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_gallery_image(request, image_id):
    image = get_object_or_404(Gallery_images, image_id=image_id)

    old_image_path = image.image.path if 'image' in request.data and image.image else None

    serializer = GalleryImageUpdateSerializer(image, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        if old_image_path and 'image' in request.data:
            if default_storage.exists(old_image_path):
                default_storage.delete(old_image_path)

        response_serializer = GalleryImageSerializer(image)
        return Response({
            'success': True,
            'message': 'Image updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from .models import Gallery_images

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_gallery_image(request, image_id):
    image = get_object_or_404(Gallery_images, image_id=image_id)

    image_info = {
        'image_id': image.image_id,
        'caption': image.caption,
        'uploaded_at': image.uploaded_at
    }

    if image.image and default_storage.exists(image.image.path):
        default_storage.delete(image.image.path)

    image.delete()

    return Response({
        'success': True,
        'message': 'Image deleted successfully',
        'deleted_image': image_info
    }, status=status.HTTP_200_OK)


#getting the images uploaded by the specific admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_gallery_images(request):
    images = Gallery_images.objects.filter(admin_id=request.user.user_id).order_by('-uploaded_at')
    serializer = GalleryImageSerializer(images, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })
#getting detailed info about a specific gallery image
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_image_detail(request, image_id):
    try:
        image = get_object_or_404(Gallery_images, image_id=image_id)
        serializer = GalleryImageSerializer(image)
        
        return Response({
            "message": "Gallery image details retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "error": "Failed to retrieve image details",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#this is for the emailing stuff
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def emailing(request):

    #type the functions here
    
    return Response({"message" : "This function uses emailing", "time": timezone.now()}, status = status.HTTP_200_OK)



