from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

class Ingredients(models.Model):
    """Модель ингедиентов для блюд."""
    name = models.CharField('Название игредиента', max_length=256)
    measurement_unit = models.CharField('Единица измерения', max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Игредиенты'
        verbose_name_plural = 'Ингредиенты'


class Tags(models.Model):
    """Модель тега."""
    name = models.CharField('Тег', max_length=256, unique=True)
    color = models.CharField('Код цвета', max_length=9)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автop'
    )
    name = models.CharField('Название блюда', max_length=256)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(Ingredients, through='IngredientRecipes', blank=True, related_name='recipes')
    tags = models.ManyToManyField(Tags, blank=True, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(validators=(MinValueValidator(1),))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class IngredientRecipes(models.Model):
    """Модель для связи ингредиента и рецепта."""
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='ingredientrecipes', verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.PROTECT, related_name='ingredientrecipes', verbose_name='Игредиент')
    amount = models.PositiveSmallIntegerField(validators=(MinValueValidator(1),))

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Состав рецепта'
    
    def __str__(self):
        return f'{self.ingredient} - {self.amount}'



class Favorite(models.Model):
    """Модель избранное."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='favorite_recipe',
                               verbose_name='Рецепт')
    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
    
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='shopping_cart_recipe',
                               verbose_name='Рецепт')
    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
    
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'