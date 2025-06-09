from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
     path('', views.read_news, name='news_list'),
     path('add/', views.add_news, name='add_news'),
]