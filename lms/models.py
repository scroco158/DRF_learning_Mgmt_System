from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название курса")
    picture = models.ImageField(
        upload_to="lms/course_preview", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название урока")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    picture = models.ImageField(
        upload_to="lms/course_preview", blank=True, null=True, verbose_name="Превью"
    )
    url = models.CharField(max_length=200, verbose_name="Видео", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
