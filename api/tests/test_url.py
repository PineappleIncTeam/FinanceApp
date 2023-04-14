from django.urls import reverse, resolve
from django.test import SimpleTestCase

from api.views import (GetCreateCategoryAPIView,
                       GetIncomeCategories,
                       GetOutcomeCategories,
                       UpdateCategory,
                       DeleteCategory,
                       AddIncomeCash,
                       UpdateIncomeCash,
                       DeleteIncomeCash,
                       AddOutcomeCash,
                       UpdateOutcomeCash,
                       DeleteOutcomeCash,
                       BalanceAPIView,
                       Last5IncomeCash,
                       Last5OutcomeCash,
                       SumIncomeCash,
                       SumIncomeCashGroup,
                       SumOutcomeCash,
                       SumOutcomeCashGroup,
                       SumMonthlyIncomeView,
                       SumMonthlyOutcomeView,
                       SumPercentMonthlyIncomeView,
                       SumPercentMonthlyOutcomeView)


class APIUrlsTest(SimpleTestCase):

    def test_url_categories(self):
        url = reverse('categories')
        self.assertEquals(resolve(url).func.view_class, GetCreateCategoryAPIView)

    def test_url_income_categories(self):
        url = reverse('income-categories')
        self.assertEquals(resolve(url).func.view_class, GetIncomeCategories)

    def test_url_outcome_categories(self):
        url = reverse('outcome-categories')
        self.assertEquals(resolve(url).func.view_class, GetOutcomeCategories)

    def test_url_update_category(self):
        url = reverse('update-category', args='1')
        self.assertEquals(resolve(url).func.view_class, UpdateCategory)

    def test_url_del_category(self):
        url = reverse('del-category', args='1')
        self.assertEquals(resolve(url).func.view_class, DeleteCategory)

    def test_url_incomecash(self):
        url = reverse('incomecash')
        self.assertEquals(resolve(url).func.view_class, AddIncomeCash)

    def test_url_update_incomecash(self):
        url = reverse('update-incomecash', args='1')
        self.assertEquals(resolve(url).func.view_class, UpdateIncomeCash)

    def test_url_delete_incomecash(self):
        url = reverse('delete-incomecash', args='1')
        self.assertEquals(resolve(url).func.view_class, DeleteIncomeCash)

    def test_url_outcomecash(self):
        url = reverse('outcomecash')
        self.assertEquals(resolve(url).func.view_class, AddOutcomeCash)

    def test_url_update_outcomecash(self):
        url = reverse('update-outcomecash', args='1')
        self.assertEquals(resolve(url).func.view_class, UpdateOutcomeCash)

    def test_url_delete_outcomecash(self):
        url = reverse('delete-outcomecash', args='1')
        self.assertEquals(resolve(url).func.view_class, DeleteOutcomeCash)

    def test_url_balance(self):
        url = reverse('balance')
        self.assertEquals(resolve(url).func.view_class, BalanceAPIView)

    def test_url_last_5_incomecash(self):
        url = reverse('last-5-incomecash')
        self.assertEquals(resolve(url).func.view_class, Last5IncomeCash)

    def test_url_last_5_outcomecash(self):
        url = reverse('last-5-outcomecash')
        self.assertEquals(resolve(url).func.view_class, Last5OutcomeCash)

    def test_url_sum_incomecash(self):
        url = reverse('sum-incomecash')
        self.assertEquals(resolve(url).func.view_class, SumIncomeCash)

    def test_url_sum_incomecash_group(self):
        url = reverse('sum-incomecash-group')
        self.assertEquals(resolve(url).func.view_class, SumIncomeCashGroup)

    def test_url_sum_outcomecash(self):
        url = reverse('sum-outcomecash')
        self.assertEquals(resolve(url).func.view_class, SumOutcomeCash)

    def test_url_sum_outcomecash_group(self):
        url = reverse('sum-outcomecash-group')
        self.assertEquals(resolve(url).func.view_class, SumOutcomeCashGroup)

    def test_url_sum_monthly_income(self):
        url = reverse('sum-monthly_income')
        self.assertEquals(resolve(url).func.view_class, SumMonthlyIncomeView)

    def test_url_sum_monthly_outcome(self):
        url = reverse('sum-monthly_outcome')
        self.assertEquals(resolve(url).func.view_class, SumMonthlyOutcomeView)

    def test_url_sum_percent_monthly_income(self):
        url = reverse('sum-percent-monthly_income')
        self.assertEquals(resolve(url).func.view_class, SumPercentMonthlyIncomeView)

    def test_url_sum_percent_monthly_outcome(self):
        url = reverse('sum-percent-monthly_outcome')
        self.assertEquals(resolve(url).func.view_class, SumPercentMonthlyOutcomeView)