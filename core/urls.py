from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('gallery/', views.get_gallery_images, name='get_gallery_images'),
    path('gallery/<str:image_id>/', views.get_gallery_image_detail, name='get_gallery_image_detail'),
    
    path('admin/gallery/upload/', views.upload_gallery_image, name='upload_gallery_image'),
    path('admin/gallery/my-images/', views.get_admin_gallery_images, name='get_admin_gallery_images'),
    path('admin/gallery/<str:image_id>/update/', views.update_gallery_image, name='update_gallery_image'),
    path('admin/gallery/<str:image_id>/delete/', views.delete_gallery_image, name='delete_gallery_image'),
    
    path('emailing/', views.emailing, name='emailing'),
]