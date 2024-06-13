from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


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

        # проверка, что модератор не может создавать и удалять
        # if self.action in ['create', 'destroy']:    # если создание или удаление
        #     self.permission_classes = [~IsModer]    # то инверсия IsModer
        # elif self.action in ['update', 'retrive']:  # если редактирование или просмотр
        #     self.permission_classes = [IsModer]     # то Is moder

        # добавление проверки, что владелец работает только со своими курсами и лекциями
        if self.action == 'create':                         # если создание
            self.permission_classes = [~IsModer]            # то инверсия IsModer (не модератор)
        elif self.action in ['update', 'retrieve']:          # если редактирование или просмотр
            self.permission_classes = [IsModer | IsOwner]   # то IsModer или IsOwner
        elif self.action == 'destroy':                      # если создание или удаление
            self.permission_classes = [~IsModer | IsOwner]  # то не IsModer или IsOwner

        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer, IsAuthenticated]

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
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)



class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | ~IsModer, IsAuthenticated)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        print(course_id)
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)  # Создаем подписку
            message = 'подписка добавлена'

        return Response({"message": message})
