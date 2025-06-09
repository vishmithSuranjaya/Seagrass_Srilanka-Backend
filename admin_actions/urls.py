from django.urls import path
from . import views

urlpatterns = [
    path('products/add/', views.add_products, name='add_products'),
    path('news/add/', views.add_news, name='add_news'),
    path('research/add/', views.add_research_articles, name='add_research_articles'),
    path('gallery/manage/', views.manage_gallery, name='manage_gallery'),
    path('delete/<str:model_name>/<str:id_value>/', views.delete_content, name='delete_content'),
]