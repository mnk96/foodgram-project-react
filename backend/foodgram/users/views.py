from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

import users.models as model
from users.serializers import CustomUserSerializers, FollowListSerializer

User = get_user_model()


class FollowViewSet(UserViewSet):
    serializer_class = CustomUserSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(page, many=True,
                                          context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError('Нельзя подписаться на себя.')
            if model.Follow.objects.filter(user=user, author=author).exists():
                raise exceptions.ValidationError(
                    'Вы уже подписаны на этого пользователя')
            model.Follow.objects.create(user=user, author=author)
            serializer = FollowListSerializer(author,
                                              context={'request': request})
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            if not model.Follow.objects.filter(user=user,
                                               author=author).exists():
                raise exceptions.ValidationError(
                    'Подписки на этого пользователя нет.')
            follow = get_object_or_404(model.Follow, user=user, author=author)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
