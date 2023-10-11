from django.contrib import admin

from users.models import FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('id', 'role', 'username', 'email')
