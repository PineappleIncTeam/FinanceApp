from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from api.models import User, Categories, IncomeCash


class CategoryURLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_category_create(self):
        url = reverse('categories')
        data = {
            "categoryName": "Test",
            "category_type": "constant",
            "income_outcome": "income",
            "is_hidden": False
        }

        # Category creation test
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Category list getting test
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)

    def test_income_categories(self):
        # Income category list test
        url = reverse('income-categories')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_outcome_categories(self):
        # Outcome category list test
        url = reverse('outcome-categories')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_money_box_category(self):
        # Money box category list test
        url = reverse('money-box-categories')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_category(self):
        # Category update test
        url = reverse('update-category', args='1')
        data = {
            "categoryName": "Test",
            "is_hidden": True
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_category = Categories.objects.get(pk=1)
        self.assertEqual(updated_category.categoryName, 'Test')
        self.assertEqual(updated_category.is_hidden, True)

    def test_delete_category(self):
        # Category delete test
        url = reverse('del-category', args='1')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Categories.DoesNotExist):
            Categories.objects.get(pk=1)


class IncomeCashAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_income_cash_create(self):
        # IncomeCash create test
        url = reverse('incomecash')
        data = {
            "sum": 5000,
            "category_id": 1,
            "category_type": "constant",
            "date": "2023-01-01"
        }

        response = self.client.post(url, data)
        updated_income_cash = IncomeCash.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(updated_income_cash.sum, 5000)
        self.assertEqual(updated_income_cash.pk, 1)
        self.assertEqual(updated_income_cash.categories.income_outcome, 'income')
        self.assertEqual(updated_income_cash.categories.category_type, 'constant')

    # def test_last_5_income_cash_get(self):
    #     # Last 5 IncomeCash test
    #     url = reverse('last-5-income-cash')
    #     income_cash1 = IncomeCash.objects.create()
