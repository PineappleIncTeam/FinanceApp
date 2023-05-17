from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from api.models import User, MoneyBox


class MoneyBoxAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_money_box_list_create(self):
        url = reverse('money-box')
        data = {
            'user': 'testuser',
            'category_id': 1,
            'box_sum': 100,
            'box_target': 1000,
            'date_created': '2023-05-17'
        }

        # Тест создания записи
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Тест получения списка записей
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_money_box(self):
        money_box = MoneyBox.objects.create(
            user=self.user,
            categories_id=1,
            box_sum=500,
            box_target=1000,
            date_created='2023-05-17'
        )
        url = reverse('update-money-box', args='1')
        data = {
            'box_sum': 700,
            'box_target': 1500
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_money_box = MoneyBox.objects.get(pk=money_box.pk)
        self.assertEqual(updated_money_box.box_sum, 700)
        self.assertEqual(updated_money_box.box_target, 1500)

    def test_delete_money_box(self):
        money_box = MoneyBox.objects.create(
            user=self.user,
            categories_id=1,
            box_sum=500,
            box_target=1000,
            date_created='2023-05-17'
        )
        url = reverse('delete-money-box', args='1')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(MoneyBox.DoesNotExist):
            MoneyBox.objects.get(pk=money_box.pk)
