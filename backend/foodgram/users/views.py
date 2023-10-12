from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

import users.models as model
from users.serializers import (FollowListSerializer,
                               FollowSerializer, CustomUserSerializers)

User = get_user_model()


class FollowViewSet(UserViewSet):
    serializer_class = CustomUserSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(page, many=True,
                                          context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', ),
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = self.request.user.id
        data = {'user': user, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        follow = get_object_or_404(model.Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
