from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_id', 'date', 'content', 'admin_id')
    list_filter = ('date', 'admin_id')
    search_fields = ('news_id', 'content')
    date_hierarchy = 'date'