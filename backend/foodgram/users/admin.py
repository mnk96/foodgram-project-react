from django.contrib import admin

from users.models import Follow, FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('id', 'role', 'username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = ('author', 'user')
    list_display = ('id', 'user', 'author')
