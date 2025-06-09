from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Media
from .serializers import MediaSerializer
from admin_actions.models import Admin

#view the photos and videos inside the media gallery
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def view_gallery(request):
    media = Media.objects.all()
    serializer = MediaSerializer(media, many = True)
    return Response(serializer.data)

#uploading media to the media table (COMMON STUFF , NOT ADMIN)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_media(request):
    if request.FILES.get('file'):
        file = request,FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        media = Media.objefcts.create(
            media_id = f"media_{timezone.now().strftime('%Y%m%d_%H%M%S')}",
            name = file.name,
            link = file_name,
            type = file.content_type,
            user_id = request.user,
        )
        serializer = MediaSerializer(media)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response({"error": "No File uploaded"}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def manage_gallery(request):
    """Admin manages gallery (add or update media)."""
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