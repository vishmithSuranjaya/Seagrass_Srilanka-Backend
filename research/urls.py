from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
    path('list/', views.research_article_list, name='research_article_list'),
    path('add/', views.add_research_articles, name='add_research_articles'),
    path('search/', views.search_research_articles, name='search_research_articles'), #Add 20/06/2025
]