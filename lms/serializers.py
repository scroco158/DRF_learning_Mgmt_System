from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    """При детальном выводе информации о курсе выводим количество уроков """
    lesson_quantity = serializers.SerializerMethodField()  # дополнительное поле

    def get_lesson_quantity(self, obj): # ??? obj это кекущий курс
        """Определяет как формируется это поле """
        return Lesson.objects.filter(course=obj.id).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lesson_quantity')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
