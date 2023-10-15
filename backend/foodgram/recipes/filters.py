from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredients, Recipes, Tags


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredients
        fields = ('name',)


class RecipesFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tags.objects.all(), field_name='tags__slug',
        to_field_name='slug')
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipes
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                shopping_cart_recipe__user=self.request.user.id)
        return queryset
