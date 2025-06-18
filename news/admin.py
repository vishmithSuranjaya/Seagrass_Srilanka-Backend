from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['news_id', 'title', 'created_at', 'is_published', 'admin_id']
    list_filter = ['created_at', 'is_published', 'admin_id']
    search_fields = ['title', 'content', 'news_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['news_id', 'created_at', 'updated_at']
    list_editable = ['is_published']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Article Information', {
            'fields': ('news_id', 'title', 'content', 'image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'admin_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('admin_id')