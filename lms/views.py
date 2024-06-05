from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        """ Выбор сериализатора"""
        if self.action == 'retrieve':     # если детальный просмотр
            return CourseDetailSerializer
        return CourseSerializer           # если все

    def perform_create(self, serializer):
        """Присвоение текущего пользователя как автора курса"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """ Проверка действий """
        if self.action in ['create', 'destroy']:    # если создание или удаление
            self.permission_classes = [~IsModer]    # то инверсия IsModer
        elif self.action in ['update', 'retrive']:  # если редактирование или просмотр
            self.permission_classes = [IsModer]     # то Is moder
        return super().get_permissions()



class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Присвоение текущего пользователя как автора урока"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
