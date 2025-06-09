from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
     path('news/', views.read_news, name='news_list'),
     path('news/add/', views.add_news, name='add_news'),
]