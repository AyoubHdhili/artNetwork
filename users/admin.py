from django.contrib import admin
from django.utils.html import format_html
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_active_badge', 'role', 'is_staff')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green; cursor: pointer;" onclick="toggleUserStatus({});">Active</span>',
                obj.pk
            )
        else:
            return format_html(
                '<span style="color: red; cursor: pointer;" onclick="toggleUserStatus({});">Inactive</span>',
                obj.pk
            )

    is_active_badge.short_description = 'Status'

    class Media:
        js = ('admin/js/toggle_user_status.js',)

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            form = self.get_form(request, form_url)(request.POST)
            if form.is_valid():
                user = form.save(commit=False) 
                user.set_password(form.cleaned_data['password'])  
                user.save()  
                return self.response_add(request, user)
        else:
            form = self.get_form(request, form_url)(request.POST)

        return super().add_view(request, form_url, extra_context)


admin.site.register(User, UserAdmin)
