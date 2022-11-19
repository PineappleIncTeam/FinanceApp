from django.db.models.aggregates import Sum, Count
from rest_framework.generics import (ListCreateAPIView,
                                     ListAPIView,
                                     CreateAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from .serializers import (CategorySerializer,
                          IncomeCashSerializer,
                          SumIncomeCashSerializer)
from .models import (Categories,
                     User,
                     IncomeCash)


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
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        category_id = self.request.data.get('category_id')
        return IncomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        serializer.save()


class Last5IncomeCash(ListAPIView):
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).order_by('-date')[:5]


class SumIncomeCash(ListAPIView):
    serializer_class = SumIncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).values('user').distinct()
    #     SUM_Constant_sum = int(
    #         IncomeCash.objects.filter(user_id=user_id).aggregate(Sum('constant_sum')).get('constant_sum__sum'))
    #     SUM_Once_sum = int(IncomeCash.objects.filter(user_id=user_id).aggregate(Sum('once_sum')).get('once_sum__sum'))
    #     sum_income_cash = IncomeCash.objects.filter(
    #         user_id=user_id,
    #         SUM_Constant_sum=SUM_Constant_sum,
    #         SUM_Once_sum=SUM_Once_sum)
    #     return sum_income_cash
