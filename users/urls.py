from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views

urlpatterns = [
    # Your existing user URLs
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/<str:user_id>/', views.update_profile, name='update_profile'),
    path('profile/change_password/<str:user_id>/',views.change_password, name='change_password'),
    path('profile/image/upload/', views.upload_profile_image, name='upload_profile_image'),
    path('profile/image/delete/', views.delete_profile_image, name='delete_profile_image'),

    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),        # login, get JWT tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # refresh access token
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # logout by blacklisting refresh token

    # url path to get any user details
    path('get_user/<str:user_id>/', views.get_user, name='get_user'),

    # Admin-only URLs
    path('admin/all/', views.list_all_users, name='list_all_users'),
    path('admin/<str:user_id>/update/', views.admin_update_user, name='admin_update_user'),
    path('admin/<str:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin/<str:user_id>/toggle-active/', views.admin_toggle_active_user, name='admin_toggle_active_user'),
    path('admin/create-admin/', views.superuser_create_admin_user, name='superuser_create_admin_user'),
]
