from django.db import models

# для избежания циклической ссылки далее используем вместо User в ForeignKey
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название курса")
    picture = models.ImageField(
        upload_to="lms/course_preview", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец", help_text="Укажите автора"
    )



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

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец", help_text="Укажите автора"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]


class Subscription(models.Model):
    """ Модель подписки на обновления курса для пользователя"""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Курс')
    is_signed = models.BooleanField(default=False, verbose_name='Признак подписки')

    def __str__(self):
        return f'{self.user}: ({self.course})'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
