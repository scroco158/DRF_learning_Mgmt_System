from django.urls import path
from rest_framework.routers import SimpleRouter
from .apps import UsersConfig
from .views import CourseViewSet

app_name = UsersConfig.name
router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
]
urlpatterns += router.urls
