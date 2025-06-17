from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/blogs/', include('blogs.urls')),
    path('api/products/', include('products.urls')),
    path('api/news/', include('news.urls')),
    path('api/research/', include('research.urls')),
    path('api/media/', include('media.urls')),
    path('api/admin/', include('admin_actions.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    