from django.urls import path
from . import views

urlpatterns = [
    path('media/upload/', views.upload_media, name='upload_image'),  
    path('media/gallery/', views.view_gallery, name='view_gallery'),
    path('media/gallery/manage/', views.manage_gallery, name='manage_gallery'),
]