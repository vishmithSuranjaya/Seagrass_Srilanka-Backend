from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('', views.read_news, name='news_list'),
    path('<str:news_id>/', views.get_news_detail, name='news_detail'),
    
    path('admin/add/', views.add_news, name='add_news'),
    path('admin/list/', views.admin_news_list, name='admin_news_list'),
    path('admin/<str:news_id>/update/', views.update_news, name='update_news'),
    path('admin/<str:news_id>/delete/', views.delete_news, name='delete_news'),

    #for google calender urls
    path("api/auth/google/login/", views.google_login, name="google-login"),
    path("api/auth/google/callback/", views.google_callback, name="google-callback"),
    path("api/calendar/events/", views.get_calendar_events, name="google-events"),
]