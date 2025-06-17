from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Users

class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ('email', 'fname', 'lname', 'user_id', 'is_staff', 'is_active', 'date_joined', 'image_preview')
    list_filter = ('is_staff','is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email' , 'password')}),
        ('personal info', {'fields' : ('fname', 'lname', 'user_id', 'image')}),
        ('permissions', {'fields' : ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('important dates', {'fields': ('last_login', 'date_joined')})
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fname', 'lname', 'password1', 'password2', 'is_active','is_staff')} 
        ),
    )
    search_fields = ('email', 'fname', 'lname')
    ordering = ('email',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Profile Image"

admin.site.register(Users,CustomUserAdmin)
 