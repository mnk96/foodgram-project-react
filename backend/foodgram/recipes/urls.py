from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import IngredientViewSet, RecipesViewSet, TagViewSet

router = SimpleRouter()
router.register('recipes', RecipesViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
