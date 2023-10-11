import base64

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

import recipes.models as models
from users.serializers import CustomUserSerializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredients
        fields = '__all__'


class IngredientRecipesReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = models.IngredientRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientRecipesWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = models.IngredientRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        return obj.name

    def get_measurement_unit(self, obj):
        return obj.measurement_unit


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipesReadSerializer(
        many=True, source='ingredientrecipes')
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializers()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return models.Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return models.ShoppingCart.objects.filter(
            user=user, recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = CustomUserSerializers(read_only=True)
    ingredients = IngredientRecipesWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tags.objects.all(), many=True)
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(validators=(MinValueValidator(1),))

    class Meta:
        model = models.Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def validate(self, value):
        tags = value.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Необходимо выбрать хотя бы один тег.')
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги должны быть уникальны.')
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо добавить хотя бы один ингредиент.')
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise serializers.ValidationError(
                    'Выбранные игредиенты не могут повторяться')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = models.Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(
                models.Ingredients, pk=ingredient['id'])
            models.IngredientRecipes.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(models.Ingredients,
                                           pk=ingredient['id'])
            models.IngredientRecipes.objects.update_or_create(
                recipe=instance, ingredient=ingredient, amount=amount)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance,
                                    context=context).data


class RecipeSubscribedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipes
        fields = ('id', 'name', 'image', 'cooking_time',)
