from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson
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

    def get_lessons_count(self, obj):
        """Определяет переменную lessons_count"""
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ('pk', 'name', 'description', 'lessons_count', 'lessons', 'owner')


class CourseDetailSerializer(ModelSerializer):
    """При детальном выводе информации о курсе выводим количество уроков """
    lesson_quantity = serializers.SerializerMethodField()  # дополнительное поле

    def get_lesson_quantity(self, obj): # ??? obj это кекущий курс
        """Определяет как формируется это поле """
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lesson_quantity')


