from django.urls import path
from django.views import View
from rest_framework.routers import SimpleRouter
from .apps import UsersConfig
from .views import CourseViewSet, UserListAPIView, UserRetrieveAPIView, UserCreateAPIView, UserUpdateAPIView, \
    UserDestroyAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name
router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('users/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>', UserDestroyAPIView.as_view(), name='user-destroy'),
]
urlpatterns += router.urls
