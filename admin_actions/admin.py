from django.contrib import admin
from .models import Admin

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'username', 'type')
    list_filter = ('type',)
    search_fields = ('admin_id', 'username')