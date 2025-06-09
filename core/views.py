from django.utils import timezone
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Admin, Blog, Product, News, Comments, Media , Cart, Payment, Research_articles
from .serializers import BlogSerializer,ProductSerializer,NewsSerializer,CommentSerializer,MediaSerializer,PaymentSerializer,ResearchArticleSerializer,CartSerializer
from users.models import Users
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

#this is for the seagrass identification tool . still not configured
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def seagrass_identification(request):


    # type the configuration of the AI model here 


    return Response({"message" : "Seagrass identification proceesed" , "time": timezone.now()}, status = status.HTTP_200_OK)


#this is for the emailing stuff
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def emailing(request):

    #type the functions here
    
    return Response({"message" : "This function uses emailing", "time": timezone.now()}, status = status.HTTP_200_OK)











#admin manages the gallery content
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def manage_gallery(request):
    if request.FILES.get('file'):
        file = request.FIES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        media = Media.objects.create(
            media_id = f"media_{timezone.now().strftime('%Y%m%d_%H%M%S')}",
            name = file.name,
            link = file_name,
            type = file.content_type,
            admin_id = Admin.objects.first()

        )
        serializer = MediaSerializer(media)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response({"error" : "No file Uploaded"}, status =  status.HTTP_400_BAD_REQUEST)




# Create your views here.
