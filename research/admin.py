from django.contrib import admin
from .models import Research_articles

@admin.register(Research_articles)
class ResearchArticlesAdmin(admin.ModelAdmin):
    list_display = ('research_id', 'link', 'admin_id')
    list_filter = ('admin_id',)
    search_fields = ('research_id', 'link')