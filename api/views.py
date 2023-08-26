from datetime import timedelta, datetime
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db.models import F

from rest_framework.generics import (ListCreateAPIView,
                                     ListAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from .serializers import (CategorySerializer,
                          IncomeCashSerializer,
                          SumIncomeCashSerializer,
                          SumIncomeGroupCashSerializer,
                          OutcomeCashSerializer,
                          SumOutcomeCashSerializer,
                          SumOutcomeGroupCashSerializer,
                          MonthlySumIncomeGroupCashSerializer,
                          MonthlySumOutcomeGroupCashSerializer,
                          MonthlySumPercentIncomeGroupCashSerializer,
                          MonthlySumPercentOutcomeGroupCashSerializer,
                          MoneyBoxSerializer,
                          SumMoneyBoxSerializer,
                          SumMoneyBoxGroupSerializer,
                          MonthlySumMoneyBoxGroupSerializer,
                          MonthlySumPercentMoneyBoxGroupSerializer,
                          ReportSerializer,
                          )
from .models import (Categories,
                     IncomeCash,
                     OutcomeCash,
                     MoneyBox)


class GetCreateCategoryAPIView(ListCreateAPIView):
    """
    Представление возвращает список всех категорий (GET)
    и создает новые категории (POST)
    Виды категорий (category_type):
        constant - постоянная
        once - разовая
        accumulate - накопления

    """

    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id)


class GetIncomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий доходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id,
                                         income_outcome='income')


class GetOutcomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id,
                                         income_outcome='outcome')


class GetMoneyBoxCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов с суммами и целями
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.pk
        money_box_cat = Categories.objects.filter(user_id=user_id, income_outcome='money_box')
        return Response(
            money_box_cat.values('categoryName', 'category_type', 'income_outcome', 'user_id', 'is_hidden')
            .annotate(sum=Sum('moneybox__sum'), target=F('moneybox__target'), category_id=F('id')))


class DeleteCategoryView(DestroyAPIView):
    """
    Удаление категории (DELETE)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)


class UpdateCategoryView(UpdateAPIView):
    """
    Изменение категории (PUT)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)


class AddIncomeCashView(ListCreateAPIView):
    """
    Представление добавляет сумму дохода в категорию
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        category_id = self.request.data.get('category_id')
        return IncomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        serializer.save()


class UpdateIncomeCashView(UpdateAPIView):
    """
    Представление изменяет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteIncomeCashView(DeleteCategoryView):
    """
    Представление удаляет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class Last5IncomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей доходов
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).order_by('-date_record')[:5]


class SumIncomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех доходов по всем категориям
    """
    serializer_class = SumIncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).values('user').distinct()


class SumIncomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех доходов в разрезе категорий
    """
    serializer_class = SumIncomeGroupCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).values('user').distinct()


class AddOutcomeCashView(ListCreateAPIView):
    """
    Представление добавляет сумму расхода в категорию
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        category_id = self.request.data.get('category_id')
        return OutcomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        serializer.save()


class UpdateOutcomeCashView(UpdateAPIView):
    """
    Представление изменяет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteOutcomeCashView(DestroyAPIView):
    """
    Представление удаляет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class SumOutcomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех расходов по всем категориям
    """
    serializer_class = SumOutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()


class SumOutcomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех расходов в разрезе категорий
    """
    serializer_class = SumOutcomeGroupCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()


class Last5OutcomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей расходов
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id).order_by('-date_record')[:5]


class BalanceAPIView(APIView):
    """
    Представление возвращает баланс пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.pk
        try:
            date_start = self.request.query_params.get('date_start')
            date_end = self.request.query_params.get('date_end')

            if date_end is None or len(date_end) <= 0:
                date_end = datetime.now()
            else:
                date_end = datetime.strptime(date_end, '%Y-%m-%d')

            if date_start is None or len(date_start) <= 0:
                date_start = date_end - timedelta(days=365)
            else:
                date_start = datetime.strptime(date_start, '%Y-%m-%d')

        except:
            d_start_outcome = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            d_end_outcome = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')
            d_start_income = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            d_end_income = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')
            d_start_money_box = MoneyBox.objects.all().order_by('date').values('date')[0].get('date')
            d_end_money_box = MoneyBox.objects.all().order_by('-date').values('date')[0].get('date')
            date_start = min(d_start_outcome, d_start_income, d_start_money_box)
            date_end = max(d_end_outcome, d_end_income, d_end_money_box)

        income_sum = IncomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        if not income_sum:
            income_sum = 0
        outcome_sum = OutcomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        if not outcome_sum:
            outcome_sum = 0
        money_box_sum = MoneyBox.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        if not money_box_sum:
            money_box_sum = 0
        balance = round(income_sum - (outcome_sum + money_box_sum), 2)
        return JsonResponse({'sum_balance': balance})


class SumMonthlyIncomeView(ListAPIView):
    """
    Представление возвращает сумму всех доходов пользователя в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumIncomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


class SumMonthlyOutcomeView(ListAPIView):
    """
    Представление возвращает сумму всех расходов пользователя в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumOutcomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


class SumPercentMonthlyIncomeView(ListAPIView):
    """
    Представление возвращает сумму всех доходов пользователя в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentIncomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


class SumPercentMonthlyOutcomeView(ListAPIView):
    """
    Представление возвращает сумму всех расходов пользователя в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentOutcomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


class AddMoneyBoxView(ListCreateAPIView):
    """
    Представление добавляет сумму накоплений
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        category_id = self.request.data.get('category_id')
        return MoneyBox.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        serializer.save()


class UpdateMoneyBoxView(UpdateAPIView):
    """
    Представление изменяет сумму накопления в категории
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteMoneyBoxView(DestroyAPIView):
    """
    Представление удаляет сумму в накоплении
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)


class SumMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений по всем категориям
    """
    serializer_class = SumMoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return MoneyBox.objects.filter(user_id=user_id).values('user').distinct()


class SumMoneyBoxGroupView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений в разрезе категорий
    """
    serializer_class = SumMoneyBoxGroupSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return MoneyBox.objects.filter(user_id=user_id).values('user').distinct()


class Last5MoneyBoxView(ListAPIView):
    """
    Представление возвращает 5 последних записей накоплений
    """
    serializer_class = MoneyBoxSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return MoneyBox.objects.filter(user_id=user_id).order_by('-id')[:5]


class SumMonthlyMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений пользователя в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumMoneyBoxGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return MoneyBox.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


class SumPercentMonthlyMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений пользователя в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentMoneyBoxGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return MoneyBox.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response([])


def date_filter(queryset, start_date=None, end_date=None):
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    return queryset


class ReportAPIView(APIView):
    """
    Представление возвращает все записи пользователя
    """
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date_start = request.query_params.get('date_start', None)
        date_end = request.query_params.get('date_end', None)

        if date_start:
            try:
                date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError('Incorrect date format for date_start, should be YYYY-MM-DD')

        if date_end:
            try:
                date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError('Incorrect date format for date_end, should be YYYY-MM-DD')

        user_id = request.user.pk
        income_cash = date_filter(IncomeCash.objects.filter(user_id=user_id), date_start, date_end).order_by(
            '-date')
        outcome_cash = date_filter(OutcomeCash.objects.filter(user_id=user_id), date_start, date_end).order_by(
            '-date')
        money_box = date_filter(MoneyBox.objects.filter(user_id=user_id), date_start, date_end).order_by('-date')

        queryset = {
            'income_cash': income_cash,
            'outcome_cash': outcome_cash,
            'money_box': money_box,
        }

        serializer = self.serializer_class(queryset, context={'request': request})
        return Response(serializer.data)
