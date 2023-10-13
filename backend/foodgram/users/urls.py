from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import FollowViewSet

router = SimpleRouter()
router.register('users', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
