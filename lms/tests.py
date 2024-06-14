
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@user.com")
        self.course = Course.objects.create(name="Test_Course", description="Курс для теста")
        self.lesson = Lesson.objects.create(name="Lesson_1", description="Урок для теста", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {
            "name": "Lesson_2",
            "url": "url youtube"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {
            "name": "Lesson_2"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Lesson_2"
        )

    def test_lesson_delete(self):
        url = reverse("lms:lesson-destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "picture": None,
                    "url": self.lesson.url,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@user.com")
        self.course = Course.objects.create(name="Test_Course", description="Курс для теста", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("lms:course_subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "подписка добавлена"})

    def test_unsubscribe(self):
        url = reverse("lms:course_subscription")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url,data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'подписка удалена'})