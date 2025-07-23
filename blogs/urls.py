from django.urls import path
from . import views

urlpatterns = [
    # Public API endpoints
    path('', views.blog_list, name='blog_list'),
    path('post/', views.post_blog, name='post_blog'),
    path('<str:blog_id>/like/', views.like_blog, name='like_blog'),
    path('create/comment/', views.create_comment, name='create_comment'),
    path('comments/<str:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('<str:blog_id>/update/', views.update_blog, name='update_blog'),
    path('<str:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('<str:blog_id>/', views.blog_reading, name='blog_reading'),

    path('admin/adminposts/', views.admin_created_blogs, name='admin_created_blogs'),
    path('admin/userposts/', views.user_created_blogs, name='user_created_blogs'),
    path('admin/post/', views.admin_post_blog, name='admin_post_blog'),
    path('admin/<str:blog_id>/update/', views.admin_update_blog, name='admin_update_blog'),
    path('admin/<str:blog_id>/delete/', views.admin_delete_blog, name='admin_delete_blog'),
    path('admin/<str:blog_id>/', views.admin_blog_detail, name='admin_blog_detail'),
]
