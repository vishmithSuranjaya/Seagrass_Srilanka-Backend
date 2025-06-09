from django.contrib import admin
from .models import Blog, Comments

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'title', 'date', 'time', 'status', 'admin_id')
    list_filter = ('date', 'admin_id', 'status')
    search_fields = ('blog_id', 'title', 'content')
    date_hierarchy = 'date'

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'blog_id', 'user_id', 'content', 'status')
    list_filter = ('blog_id', 'user_id', 'status')
    search_fields = ('comment_id', 'content')