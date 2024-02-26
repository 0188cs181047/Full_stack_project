from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser ,AppName ,StudentUser, TeacherUser



@admin.register(AppName)
class AppNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions', 'app_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'app_name')}
        ),
    )
    search_fields = ['username', 'email']
    ordering = ['id']


admin.site.register(StudentUser)
admin.site.register(TeacherUser)

