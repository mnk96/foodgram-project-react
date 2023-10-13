from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import users.models as model
from users.serializers import (FollowListSerializer,
                               FollowSerializer, CustomUserSerializers)


class FollowViewSet(UserViewSet):
    serializer_class = CustomUserSerializers

    def get_queryset(self):
        return model.FoodgramUser.objects.all()

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        queryset = model.FoodgramUser.objects.filter(
            following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(page, many=True,
                                          context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', ),
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        data = {'user': self.request.user.id, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(model.User, pk=id)
        follow = get_object_or_404(model.Follow,
                                   user=self.request.user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
