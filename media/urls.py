from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_media, name='upload_image'),  
    path('gallery/', views.view_gallery, name='view_gallery'),
    path('gallery/manage/', views.manage_gallery, name='manage_gallery'),
]