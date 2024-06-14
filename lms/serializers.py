from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    # Использую валидатор для проверки адреса видео урока
    url = serializers.CharField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    # перечень лекций текущего курса
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    # количество лекций текущего курса
    lessons_count = serializers.SerializerMethodField()
    have_subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        """Определяет переменную lessons_count"""
        return obj.lesson_set.count()

    def get_have_subscription(self, instance):
        """ Проверяет есть ли подписка на курс у текущего пользователя"""
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()

    class Meta:
        model = Course
        fields = ('pk', 'name', 'description', 'owner', 'have_subscription', 'lessons_count', 'lessons')


class CourseDetailSerializer(ModelSerializer):
    """При детальном выводе информации о курсе выводим количество уроков """
    lesson_quantity = serializers.SerializerMethodField()  # дополнительное поле

    def get_lesson_quantity(self, obj): # ??? obj это кекущий курс
        """Определяет как формируется это поле """
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lesson_quantity')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
