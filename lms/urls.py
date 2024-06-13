from django.urls import path
from rest_framework.routers import SimpleRouter
from lms.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView, \
    LessonRetrieveAPIView, SubscriptionCreateAPIView
from .apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()

router.register("", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-destroy"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),

    path("course/subscribe/", SubscriptionCreateAPIView.as_view(), name="course_subscription"),
]
urlpatterns += router.urls
