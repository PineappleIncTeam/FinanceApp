from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from api.models import User, MoneyBox
from api.views import MoneyBoxView, DeleteMoneyBox


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
    pass
