from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from task.models import Task

User = get_user_model()


class TestTaskRetrieveUpdateDestroyAPIView(APITestCase):
    USER_1 = dict(
        username="username_1",
        password="fake_password",
    )
    USER_2 = dict(
        username="username_2",
        password="fake_password",
    )

    @classmethod
    def setUpTestData(cls):
        """
        Делаем двух пользователей в БД.
        Каждому из них назначаем по записи.
        """
        users = [
            User(**cls.USER_1),
            User(**cls.USER_2),
        ]
        User.objects.bulk_create(users)
        cls.db_user_1 = users[0]

        tasks = [
            Task(title="title_1", author=users[0]),
            Task(title="title_2", author=users[1]),
        ]
        Task.objects.bulk_create(tasks)

    def setUp(self) -> None:
        """При каждом тестовом методе, будем делать нового клиента и авторизовать его."""
        self.auth_user_1 = APIClient()
        self.auth_user_1.force_authenticate(user=self.db_user_1)  # так как не интересуют сами механизмы авторизации, авторизуем нашего пользователя принудительно

    def test_get(self):
        task_pk = 1
        url = f"/api/v1/tasks/{task_pk}/"
        resp = self.auth_user_1.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_partial_update_other_task(self):
        task_pk = 2
        url = f"/api/v1/tasks/{task_pk}/"
        resp = self.auth_user_1.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_task(self):
        task_pk = 2
        data = {
            "title": "fake_title",
        }
        url = f"/api/v1/tasks/{task_pk}/"
        resp = self.auth_user_1.put(url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
