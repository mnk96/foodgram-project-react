from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

import recipes.models as model
import recipes.serializers as serializer
from recipes.filters import IngredientFilter, RecipesFilter
from recipes.permissions import IsAuthorOrAuthenticated
from recipes.serializers import FavoriteSerializer, ShoppingCartSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тега."""
    queryset = model.Ingredients.objects.all()
    serializer_class = serializer.IngredientSerializer
    permission_classes = (IsAuthorOrAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """Вьюсет для рецепта."""
    queryset = model.Recipes.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    permission_classes = (IsAuthorOrAuthenticated, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializer.RecipeReadSerializer
        return serializer.RecipeWriteSerializer

    @action(detail=True, methods=('post', ),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = self.request.user.id
        data = {'user': user, 'recipe': pk}
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(model.Recipes, pk=pk)
        favorite = get_object_or_404(model.Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post', ),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = self.request.user.id
        data = {'user': user, 'recipe': pk}
        serializer = ShoppingCartSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(model.Recipes, pk=pk)
        shopping_cart = get_object_or_404(model.ShoppingCart,
                                          user=user, recipe=recipe)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('get', ),
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_cart = model.ShoppingCart.objects.filter(user=user)
        list = ['Список покупок:\n']
        id = []
        for recipe in shopping_cart:
            id.append(recipe.recipe.id)
        ingredients = model.IngredientRecipes.objects.filter(
            recipe__in=id).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                ingredient__amount=Sum('amount'))
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            amount = ingredient['ingredient__amount']
            measurement_unit = ingredient['ingredient__measurement_unit']
            list.append(f'{name} - {amount} {measurement_unit}\n')
        responce = HttpResponse(list, content_type='text/plain')
        responce['Content-Disposition'] = (
            'attachment;filename=shopping_list.txt')
        return responce


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тега."""
    queryset = model.Tags.objects.all()
    serializer_class = serializer.TagSerializer
    permission_classes = (IsAuthorOrAuthenticated,)
    pagination_class = None
