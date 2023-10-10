from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    """Модель пользователя."""
    class Roles(models.TextChoices):
        """Роли пользователей."""
        USER = 'user', 'user'
        ADMIN = 'admin', 'admin'

    username = models.CharField('Логин', max_length=150, unique=True, null=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True)
    role = models.CharField(max_length=9, choices=Roles.choices, blank=True,
                            null=True, default=Roles.USER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(FoodgramUser, on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(FoodgramUser,on_delete=models.CASCADE,
        related_name='following')
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

