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

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit is not None:
            recipes = Recipes.objects.filter(author=obj)[:int(recipes_limit)]
        else:
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

    def validate(self, value):
        user = value['user']
        follow = value['author']
        if user == follow:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        if Follow.objects.filter(author=follow, user=user).exists():
            raise serializers.ValidationError('Нельзя подписаться второй раз')
        return value

    def to_representation(self, instance):
        return FollowListSerializer(instance.author, context=self.context).data
