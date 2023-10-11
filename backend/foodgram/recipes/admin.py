from django.contrib import admin

import recipes.models as model


@admin.register(model.Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name__startswith', )


@admin.register(model.Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = ('id', 'name', 'author')
    search_fields = ('name__startswith', )
    readonly_fields = ('in_favorite',)

    def in_favorite(self, obj):
        return obj.favorite_recipe.all().count()


@admin.register(model.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(model.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(model.ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(model.IngredientRecipes)
class IngredientRecipesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
