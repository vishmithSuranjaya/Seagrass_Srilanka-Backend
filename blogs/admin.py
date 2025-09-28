from django.contrib import admin
from .models import Blog, Comments

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'blog_id', 'user_id', 'content', 'status')
    list_filter = ('blog_id', 'user_id', 'status')
    search_fields = ('comment_id', 'content')