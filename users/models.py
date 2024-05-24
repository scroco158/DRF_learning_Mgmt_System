from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        max_length=50, unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Payment(models.Model):
    """ Оплата за курс или урок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    p_date = models.DateField(verbose_name='Дата оплаты')
    сourse = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='За курс', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='За урок', null=True, blank=True)
    method = models.CharField(max_length=20, verbose_name='Способ оплаты')

    def __str__(self):
        return self.method

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'

