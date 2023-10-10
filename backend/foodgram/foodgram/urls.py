from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipesViewSet, TagViewSet, IngredientViewSet
from users.views import FollowViewSet

router = SimpleRouter()
router.register('recipes', RecipesViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('users', FollowViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
