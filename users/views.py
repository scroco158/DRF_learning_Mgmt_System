from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """ Создание пользователя (регистрация) """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)  # для этого контроллера доступ для всех

    def perform_create(self, serializer):
        """ Создание пароля"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['course', 'lesson']
    ordering_fields = ['p_date',]
    serializer_class = PaymentSerializer
