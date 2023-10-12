# from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import foodgram.constants as const

User = get_user_model()


class Ingredients(models.Model):
    """Модель ингедиентов для блюд."""
    name = models.CharField('Название игредиента', max_length=const.MAX_LENGTH)
    measurement_unit = models.CharField('Единица измерения', max_length=const.MAX_MESURE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Игредиенты'
        verbose_name_plural = 'Ингредиенты'
        constraints = (models.UniqueConstraint(
            fields=('name', 'measurement_unit'),
            name = 'unique_ingredient'
        ),)


class Tags(models.Model):
    """Модель тега."""
    name = models.CharField('Тег', max_length=const.MAX_LENGTH, unique=True)
    color = models.CharField('Код цвета', max_length=9)
    # color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автop')
    name = models.CharField('Название блюда', max_length=const.MAX_LENGTH)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True
    )
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredients, through='IngredientRecipes',
        blank=True, related_name='recipes')
    tags = models.ManyToManyField(Tags, blank=True, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(const.MIN_VALUE),
                    MaxValueValidator(const.MAX_VALUE)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipes(models.Model):
    """Модель для связи ингредиента и рецепта."""
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredients, on_delete=models.PROTECT,
        related_name='ingredientrecipes',
        verbose_name='Игредиент')
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(const.MIN_VALUE),
                    MaxValueValidator(const.MAX_VALUE)])

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Состав рецепта'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class AddRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, verbose_name='Рецепт')
    class Meta:
        abstract = True


class Favorite(AddRecipe):
    """Модель избранное."""
    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorite_recipe'


class ShoppingCart(AddRecipe):
    """Модель списка покупок."""
    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        default_related_name = 'shopping_cart_recipe'
