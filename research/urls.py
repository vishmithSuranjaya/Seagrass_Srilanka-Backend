from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
    path('research-articles/list/', views.research_article_list, name='research_article_list'),
    path('research-articles/add/', views.add_research_articles, name='add_research_articles'),
]