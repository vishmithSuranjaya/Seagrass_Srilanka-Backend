from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/post/', views.post_blog, name='post_blog'),
    path('blogs/<str:blog_id>/like/', views.like_blog, name='like_blog'),
    path('blogs/<str:blog_id>/', views.blog_reading, name='blog_reading'),
    path('blogs/comments/', views.create_comment, name='create_comment'),
    path('blogs/comments/<str:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
]