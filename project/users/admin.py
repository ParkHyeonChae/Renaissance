from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 
        'name', 
        'location',
        'sns',
        'genre',
        'position', 
        'level',
        'registered_date'
        )
    search_fields = ('user_id', 'name', 'genre', 'position')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)