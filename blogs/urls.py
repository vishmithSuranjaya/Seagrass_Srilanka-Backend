from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
    path('', views.blog_list, name='blog_list'),
    path('post/', views.post_blog, name='post_blog'),
    path('<str:blog_id>/like/', views.like_blog, name='like_blog'),
    
    path('create/comment/', views.create_comment, name='create_comment'),
    path('comments/<str:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('<str:blog_id>/update/', views.update_blog, name='update-blog'),
    path('<str:blog_id>/delete/', views.delete_blog, name='delete-blog'),
    path('<str:blog_id>/', views.blog_reading, name='blog_reading'),

]   