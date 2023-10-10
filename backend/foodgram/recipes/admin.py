from django.contrib import admin
import recipes.models as model

admin.site.register(model.Ingredients)
admin.site.register(model.Tags)
admin.site.register(model.Favorite)
admin.site.register(model.ShoppingCart)
admin.site.register(model.Recipes)
admin.site.register(model.IngredientRecipes)
