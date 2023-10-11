from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipes
from users.models import Follow, FoodgramUser


class CustomUserSerializers(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    recipes_count = serializers.ReadOnlyField(source='recipes.count')
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def validate(self, value):
        author = self.instance
        user = self.context.get('request').user
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('Нельзя подписаться повторно.')
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        return value

    def get_recipes(self, obj):
        recipes = Recipes.objects.filter(author=obj)
        return FollowRecipeSerializer(recipes, many=True,
                                      context=self.context).data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate_author(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        if Follow.objects.filter(author=value, user=user).exists():
            raise serializers.ValidationError('Нельзя подписаться второй раз')
        return value

    def to_representation(self, instance):
        return FollowListSerializer(instance.author, context=self.context).data
