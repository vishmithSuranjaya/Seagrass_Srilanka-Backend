from django.contrib import admin
from .models import Gallery_images

@admin.register(Gallery_images)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'caption', 'admin_id', 'uploaded_at')
    list_filter = ('uploaded_at', 'admin_id')
    search_fields = ('caption', 'image_id', 'admin_id__username')
    readonly_fields = ('image_id', 'uploaded_at')
    ordering = ('-uploaded_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('admin_id',)
        return self.readonly_fields