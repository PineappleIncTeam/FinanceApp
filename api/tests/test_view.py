from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from api.models import User, MoneyBox
from api.views import MoneyBoxView, UpdateMoneyBox, DeleteMoneyBox


class CategoryAPIViewTest(TestCase):
    pass


class GetIncomeCategoriesAPIViewTest(TestCase):
    pass


class GetOutcomeCategoriesAPIViewTest(TestCase):
    pass


class UpdateCategoryAPIViewTest(TestCase):
    pass


class DeleteCategoryAPIViewTest(TestCase):
    pass


class AddIncomeCashAPIViewTest(TestCase):
    pass


class UpdateIncomeCashAPIViewTest(TestCase):
    pass


class DeleteIncomeCashAPIViewTest(TestCase):
    pass


class Last5IncomeCashAPIViewTest(TestCase):
    pass


class SumIncomeCashAPIVIewTest(TestCase):
    pass


class SumIncomeCashGroupAPIViewTest(TestCase):
    pass


class AddOutcomeCashAPIViewTest(TestCase):
    pass


class UpdateOutcomeCashAPIViewTest(TestCase):
    pass


class DeleteOutcomeCashAPIViewTest(TestCase):
    pass


class SumOutcomeCashAPIVIewTest(TestCase):
    pass


class SumOutcomeCashGroupAPIViewTest(TestCase):
    pass


class Last5OutcomeCashAPIViewTest(TestCase):
    pass


class BalanceAPIView(TestCase):
    pass


class SumMonthlyIncomeAPITest(TestCase):
    pass


class SumMonthlyOutcomeAPIViewTest(TestCase):
    pass


class SumPercentMonthlyIncomeAPIViewTest(TestCase):
    pass


class SumPercentMonthlyOutcomeAPIViewTest(TestCase):
    pass


class MoneyBoxViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.moneybox = MoneyBox.objects.create(user=self.user, box_sum=100, box_target=200, date_created='2023-05-15')

    def test_get_moneybox_list(self):
        request = self.factory.get('/money-box/')
        force_authenticate(request, user=self.user)
        view = MoneyBoxView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['box_sum'], 100)
        self.assertEqual(response.data[0]['box_target'], 200)

    def test_create_moneybox(self):
        request = self.factory.post('/money-box/', {'box_sum': 150, 'box_target': 300, 'date_created': '2023-05-05'})
        force_authenticate(request, user=self.user)
        view = MoneyBoxView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MoneyBox.objects.count(), 1)

    def test_partial_update_moneybox(self):
        request = self.factory.patch(f'/update-money-box/{self.moneybox.id}/', {'box_sum': 200})
        force_authenticate(request, user=self.user)
        view = UpdateMoneyBox.as_view()
        response = view(request, pk=self.moneybox.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['box_sum'], 200)
        self.moneybox.refresh_from_db()
        self.assertEqual(self.moneybox.box_sum, 200)

    def test_delete_moneybox(self):
        request = self.factory.delete(f'/delete-money-box/{self.moneybox.id}/')
        force_authenticate(request, user=self.user)
        view = DeleteMoneyBox.as_view()
        response = view(request, pk=self.moneybox.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MoneyBox.objects.filter(pk=self.moneybox.id).exists())
