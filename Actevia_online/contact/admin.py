from django.contrib import admin

# Register your models here.

from.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email','name','is_resolved','created_at')
    list_editable = ('is_resolved',)
    list_filter = ('is_resolved','created_at')





admin.site.register(Contact,ContactAdmin)

