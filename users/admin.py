from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ('email', 'fname', 'lname', 'user_id', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff','is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email' , 'password')}),
        ('personal info', {'fields' : ('fname', 'lname', 'user_id')}),
        ('permissions', {'fields' : ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('important dates', {'fields': ('last_login', 'date_joined')})
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fname', 'lname', 'password1', 'password2', 'is_active','is_staff')} 
        ),
1    )
    search_fields = ('email', 'fname', 'lname')
    ordering = ('email',)

admin.site.register(Users,CustomUserAdmin)


        
    
# Register your models here.
