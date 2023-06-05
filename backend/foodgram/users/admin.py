from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Follow


class MyUserAdmin(UserAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email')
    list_filter = ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user',)
