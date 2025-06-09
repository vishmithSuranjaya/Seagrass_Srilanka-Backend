from django.contrib import admin
from .models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'name', 'link', 'type', 'user_id', 'admin_id')
    list_filter = ('type', 'user_id', 'admin_id')
    search_fields = ('media_id', 'name', 'link')