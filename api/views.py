from django.db.models.aggregates import Sum, Count
from django.http import JsonResponse
from datetime import datetime, date
from rest_framework.generics import (ListCreateAPIView,
                                     ListAPIView,
                                     CreateAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import (CategorySerializer,
                          IncomeCashSerializer,
                          OutcomeCashSerializer,
                          SumIncomeCashSerializer,
                          SumOutcomeCashSerializer,
                          SumIncomeGroupCashSerializer,
                          SumOutcomeGroupCashSerializer)
from .models import (Categories,
                     User,
                     IncomeCash,
                     OutcomeCash)


class GetCreateCategoryAPIView(ListCreateAPIView):
    """
    Представление возвращает список всех категорий (GET)
    и создает новые категории (POST)
    Виды категорий (category_type):
        constant - постоянная
        once - разовая

    """

    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id)


class GetIncomeCategories(ListAPIView):
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


class GetOutcomeCategories(ListAPIView):
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


class DeleteCategory(DestroyAPIView):
    """
    Удаление категории (DELETE)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)


class UpdateCategory(UpdateAPIView):
    """
    Изменение категории (PUT)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)


class AddIncomeCash(ListCreateAPIView):
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


class UpdateIncomeCash(UpdateAPIView):
    """
    Представление изменяет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteIncomeCash(DeleteCategory):
    """
    Представление удаляет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class Last5IncomeCash(ListAPIView):
    """
    Представление возвращает 5 последних записей доходов
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).order_by('-date_record')[:5]


class SumIncomeCash(ListAPIView):
    """
    Представление возвращает сумму всех доходов по всем категориям
    """
    serializer_class = SumIncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).values('user').distinct()


class SumIncomeCashGroup(ListAPIView):
    """
    Представление возвращает сумму всех доходов в разрезе категорий
    """
    serializer_class = SumIncomeGroupCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).values('user').distinct()


class AddOutcomeCash(ListCreateAPIView):
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


class UpdateOutcomeCash(UpdateAPIView):
    """
    Представление изменяет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteOutcomeCash(DestroyAPIView):
    """
    Представление удаляет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)


class SumOutcomeCash(ListAPIView):
    """
    Представление возвращает сумму всех расходов по всем категориям
    """
    serializer_class = SumOutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()


class SumOutcomeCashGroup(ListAPIView):
    """
    Представление возвращает сумму всех расходов в разрезе категорий
    """
    serializer_class = SumOutcomeGroupCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()


class Last5OutcomeCash(ListAPIView):
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
            date_start = datetime.strptime(self.request.query_params.get('date_start'), '%Y-%m-%d').date()
            date_end = datetime.strptime(self.request.query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            d_start_outcome = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            d_end_outcome = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')
            d_start_income = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            d_end_income = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')
            date_start = min(d_start_outcome, d_start_income)
            date_end = max(d_end_outcome, d_end_income)

        income_sum = IncomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        if not income_sum:
            income_sum = 0
        outcome_sum = OutcomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        if not outcome_sum:
            outcome_sum = 0
        balance = round(income_sum - outcome_sum, 2)
        return JsonResponse({'sum_balance': balance})
