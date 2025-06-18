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

#uploading a new image by the admin
@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_gallery_image(request):
    try:
        try:
            admin = Admin.objects.get(username=request.user.username)
        except Admin.DoesNotExist:
            return Response({
                "error": "Admin profile not found for this user"
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['image_id'] = str(uuid.uuid4())[:10]  
        data['admin_id'] = admin.admin_id
        
        serializer = GalleryImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Image uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            "error": "Failed to upload image",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#update image caption or replace the image
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_gallery_image(request, image_id):
    try:
        image = get_object_or_404(Gallery_images, image_id=image_id)
        
        try:
            admin = Admin.objects.get(username=request.user.username)
        except Admin.DoesNotExist:
            return Response({
                "error": "Admin profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        old_image_path = None
        if 'image' in request.data and image.image:
            old_image_path = image.image.path
        
        serializer = GalleryImageUpdateSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            if old_image_path and 'image' in request.data:
                try:
                    if default_storage.exists(old_image_path):
                        default_storage.delete(old_image_path)
                except Exception as e:
                    print(f"Failed to delete old image: {e}")
            
            updated_image = Gallery_images.objects.get(image_id=image_id)
            response_serializer = GalleryImageSerializer(updated_image)
            
            return Response({
                "message": "Image updated successfully",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            "error": "Failed to update image",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#deleting a gallery image
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_gallery_image(request, image_id):
    try:
        image = get_object_or_404(Gallery_images, image_id=image_id)
        
        try:
            admin = Admin.objects.get(username=request.user.username)
        except Admin.DoesNotExist:
            return Response({
                "error": "Admin profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        image_info = {
            "image_id": image.image_id,
            "caption": image.caption,
            "uploaded_at": image.uploaded_at
        }
        
        if image.image:
            try:
                if default_storage.exists(image.image.path):
                    default_storage.delete(image.image.path)
            except Exception as e:
                print(f"Failed to delete image file: {e}")
        
        image.delete()
        
        return Response({
            "message": "Image deleted successfully",
            "deleted_image": image_info
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "error": "Failed to delete image",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#getting the images uploaded by the specific admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_gallery_images(request):
    try:
        try:
            admin = Admin.objects.get(username=request.user.username)
        except Admin.DoesNotExist:
            return Response({
                "error": "Admin profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        images = Gallery_images.objects.filter(admin_id=admin).order_by('-uploaded_at')
        serializer = GalleryImageSerializer(images, many=True)
        
        return Response({
            "message": "Admin gallery images retrieved successfully",
            "data": serializer.data,
            "count": images.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "error": "Failed to retrieve admin gallery images",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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



