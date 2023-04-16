from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from api.models import IncomeCash, OutcomeCash


class CategoryAPIViewTest(APITestCase):
    url = reverse('categories')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            "categoryName": "CatName",
            "category_type": "constant",
            "income_outcome": "income"
        }

    def tearDown(self):
        pass

    def test_get_category_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_category_is_authenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['categoryName'], 'CatName')

    def test_post_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetIncomeCategoriesAPIViewTest(APITestCase):
    url = reverse('income-categories')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_get_income_category_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_income_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetOutcomeCategoriesAPIViewTest(APITestCase):
    outcome_category_url = reverse('outcome-categories')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_get_outcome_category_is_authenticated(self):
        response = self.client.get(self.outcome_category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_outcome_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.outcome_category_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateCategoryAPIViewTest(APITestCase):
    url = reverse('update-category', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            "categoryName": "CatName",
            "category_type": "constant",
            "income_outcome": "income"
        }

    def tearDown(self):
        pass

    def test_put_category_is_authenticated(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteCategoryAPIViewTest(APITestCase):
    url = reverse('del-category', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_del_category_is_authenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_del_category_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AddIncomeCashAPIViewTest(APITestCase):
    url = reverse('incomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
            "date": "2023-04-15"
        }

    def tearDown(self):
        pass

    def test_get_incomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncomeCash.objects.get(sum=10000))

    def test_get_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_incomecash_is_authenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        outcomecash = IncomeCash.objects.get(id=self.incomecash.id)
        outcomecash.sum += Decimal(self.data['sum'])
        outcomecash.save()
        self.assertEqual(outcomecash.sum, 15000)

    def test_post_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateIncomeCashAPIViewTest(APITestCase):
    url = reverse('update-incomecash', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
        }

    def tearDown(self):
        pass

    def test_put_incomecash_is_authenticated(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncomeCash.objects.get(sum=5000))

    def test_put_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteIncomeCashAPIViewTest(APITestCase):
    url = reverse('delete-incomecash', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
        }

    def tearDown(self):
        pass

    def test_delete_incomecash_is_authenticated(self):
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Last5IncomeCashAPIViewTest(APITestCase):
    url = reverse('last-5-incomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_last5_incomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncomeCash.objects.get(sum=10000))

    def test_get_last5_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SumIncomeCashAPIVIewTest(APITestCase):
    url = reverse('sum-incomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_sum_incomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncomeCash.objects.get(sum=10000))

    def test_get_sum_incomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SumIncomeCashGroupAPIViewTest(APITestCase):
    url = reverse('sum-incomecash-group')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_sum_incomecash_group_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IncomeCash.objects.get(sum=10000))

    def test_get_sum_incomecash_group_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AddOutcomeCashAPIViewTest(APITestCase):
    url = reverse('outcomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
            "date": "2023-04-15"
        }

    def tearDown(self):
        pass

    def test_get_outcomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OutcomeCash.objects.get(sum=10000))

    def test_get_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_outcomecash_is_authenticated(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        outcomecash = OutcomeCash.objects.get(id=self.outcomecash.id)
        outcomecash.sum += Decimal(self.data['sum'])
        outcomecash.save()
        self.assertEqual(outcomecash.sum, 15000)

    def test_post_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateOutcomeCashAPIViewTest(APITestCase):
    url = reverse('update-outcomecash', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
        }

    def tearDown(self):
        pass

    def test_put_outcomecash_is_authenticated(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OutcomeCash.objects.get(sum=5000))

    def test_put_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteOutcomeCashAPIViewTest(APITestCase):
    url = reverse('delete-outcomecash', args='1')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.data = {
            "category_id": 1,
            "sum": "5000",
        }

    def tearDown(self):
        pass

    def test_delete_outcomecash_is_authenticated(self):
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SumOutcomeCashAPIVIewTest(APITestCase):
    url = reverse('sum-outcomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_sum_outcomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OutcomeCash.objects.get(sum=10000))

    def test_get_sum_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SumOutcomeCashGroupAPIViewTest(APITestCase):
    url = reverse('sum-outcomecash-group')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_sum_outcomecash_group_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OutcomeCash.objects.get(sum=10000))

    def test_get_sum_outcomecash_group_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Last5OutcomeCashAPIViewTest(APITestCase):
    url = reverse('last-5-outcomecash')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_last5_outcomecash_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OutcomeCash.objects.get(sum=10000))

    def test_get_last5_outcomecash_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BalanceAPIView(APITestCase):
    url = reverse('balance')

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='TestUser', password='very-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.incomecash = IncomeCash.objects.create(user=self.user, sum=10000, date='2023-04-15')
        self.outcomecash = OutcomeCash.objects.create(user=self.user, sum=5000, date='2023-04-15')

    def tearDown(self):
        pass

    def test_get_balance_is_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.json()['sum_balance']), 5000.00)
        balance = self.incomecash.sum - self.outcomecash.sum
        self.assertEqual(balance, 5000)

    def test_get_balance_is_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SumMonthlyIncomeViewAPITest(APITestCase):
    pass


class SumMonthlyOutcomeViewAPIViewTest(APITestCase):
    pass


class SumPercentMonthlyIncomeViewAPIViewTest(APITestCase):
    pass


class SumPercentMonthlyOutcomeViewAPIViewTest(APITestCase):
    pass
