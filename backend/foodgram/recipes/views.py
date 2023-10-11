from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

import recipes.models as model
import recipes.serializers as serializer
from recipes.filters import IngredientFilter, RecipesFilter
from recipes.permissions import IsAdminOrReadOnly
from recipes.serializers import RecipeSubscribedSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тега."""
    queryset = model.Ingredients.objects.all()
    serializer_class = serializer.IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """Вьюсет для рецепта."""
    queryset = model.Recipes.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializer.RecipeReadSerializer
        return serializer.RecipeWriteSerializer

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(model.Recipes, pk=pk)
        if self.request.method == 'POST':
            if model.Favorite.objects.filter(user=user,
                                             recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепт уже в избранном')
            model.Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscribedSerializer(
                recipe, context={'request': request})
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            if not model.Favorite.objects.filter(user=user,
                                                 recipe=recipe).exists():
                raise exceptions.ValidationError('Рецептa нет в избранном')
            favorite = get_object_or_404(
                model.Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(model.Recipes, pk=pk)
        if self.request.method == 'POST':
            if model.ShoppingCart.objects.filter(user=user,
                                                 recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепт уже в списке покупок')
            model.ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscribedSerializer(
                recipe, context={'request': request})
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            if not model.ShoppingCart.objects.filter(user=user,
                                                     recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецептa нет в списке покупок')
            shopping_cart = get_object_or_404(model.ShoppingCart,
                                              user=user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=('get', ),
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_cart = model.ShoppingCart.objects.filter(user=user)
        print(shopping_cart)
        list = ['Список покупок:\n']
        id = []
        for recipe in shopping_cart:
            id.append(recipe.recipe.id)
        print(id)
        ingredients = model.IngredientRecipes.objects.filter(
            recipe__in=id).values(
            'ingredient__name', 'ingredient__measurement_unit'
            ).annotate(ingredient__amount=Sum('amount'))
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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
