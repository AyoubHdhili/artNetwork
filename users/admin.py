from django.contrib import admin
from .models import User
from django.utils.html import format_html 

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_active_badge', 'role', 'is_staff')
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; cursor: pointer;" onclick="toggleUserStatus({});">Active</span>', obj.pk)
        else:
            return format_html('<span style="color: red; cursor: pointer;" onclick="toggleUserStatus({});">Inactive</span>', obj.pk)

    is_active_badge.short_description = 'Status'
    
    class Media:
        js = ('admin/js/toggle_user_status.js',)  

admin.site.register(User, UserAdmin)
