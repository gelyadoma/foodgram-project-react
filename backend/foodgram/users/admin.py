from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email')
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user',)
