import logging

from datetime import timedelta, datetime
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.db.models import F
from django.contrib.auth import get_user_model

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

User = get_user_model()

logger = logging.getLogger(__name__)


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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] created '
            f'category {serializer.instance}')

    def get_queryset(self):
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested '
                f'a list of all categories')
            query_result = Categories.objects.filter(
                user_id=self.request.user.pk
            )
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'a list of all categories')
            return query_result

        except Exception as e:
            logger.error(
                f'Request a list of all categories '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}')
            return []


class UpdateCategoryView(UpdateAPIView):
    """
    Изменение категории (PUT)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        category = self.get_object()

        try:
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested to update "
                f"category [ID: {category.pk}, "
                f"name: {category.categoryName}].")

            response = super().update(request, *args, **kwargs)

            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully updated "
                f"category [ID: {category.pk}, "
                f"name: {category.categoryName}].")
            return response

        except Exception as e:
            logger.error(
                f"Updating category [ID: {category.pk}, "
                f"name: {category.categoryName}] "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] failed with error: {e}.")
            raise


class DeleteCategoryView(DestroyAPIView):
    """
    Удаление категории (DELETE)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()

        try:

            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested to delete "
                f"category [ID: {category.pk}, "
                f"name: {category.categoryName}]")

            response = super(DeleteCategoryView, self). \
                delete(request, *args, **kwargs)

            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully deleted "
                f"category [ID: {category.pk}, "
                f"name: {category.categoryName}].")

            return response

        except Exception as e:
            logger.error(
                f"Deleting category [ID: {category.pk}, "
                f"name: {category.categoryName}] "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class GetIncomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий доходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested "
                f"a list of the 'Income' categories.")
            query_result = Categories.objects.filter(
                user_id=self.request.user.pk,
                income_outcome='income'
            )
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of the 'Income' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Income' categories "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}")
            raise


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
        return IncomeCash.objects.filter(
            user_id=user_id,
            categories_id=category_id
        )

    def perform_create(self, serializer):
        category_name = Categories.objects.get(
            pk=self.request.data.get("category_id")).categoryName
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested to create amount '
                f'in income category '
                f'[ID: {self.request.data.get("category_id")}, '
                f'name: {category_name}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in income category '
                f'[ID: {self.request.data.get("category_id")}, '
                f'name: {category_name}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] failed with error: {e}.')
            raise

        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] successfully added in '
            f'income [ID: {saved_object.pk}, '
            f'amount: {saved_object.sum}] '
            f'in category [ID: {saved_object.categories.pk}, '
            f'name: {saved_object.categories.categoryName}].')


class Last5IncomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей доходов
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested for "
            f"a list of 5 last Incomes")

        try:
            quesry_result = IncomeCash.objects.filter(
                user_id=self.request.user.pk).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of 5 last Incomes.")
            return quesry_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Incomes "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}")
            raise


class SumIncomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех доходов по всем категориям
    """
    serializer_class = SumIncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested "
            f"the amount of all income in all categories.")

        try:
            query_result = IncomeCash.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all income in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all income in all "
                f"categories for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}")
            raise


class SumIncomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех доходов в разрезе категорий
    """
    serializer_class = SumIncomeGroupCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested the amount "
            f"of all income in the context of categories.")

        try:
            query_result = IncomeCash.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all income in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all income in the "
                f"context of categories for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}")
            raise


class SumMonthlyIncomeView(ListAPIView):
    """
    Представление возвращает сумму всех доходов пользователя
    в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumIncomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return IncomeCash.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all income in the context of categories '
            f'with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all income in the context of '
                f'categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all income in the '
                f'context of categories with a division by month '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}')
        raise


class SumPercentMonthlyIncomeView(ListAPIView):
    """
    Представление возвращает сумму всех доходов пользователя
    в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentIncomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return IncomeCash.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all income in the context of categories '
            f'with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all income in the context of '
                f'categories with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all income in the '
                f'context of categories with a division by month '
                f'as a percentage for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}')
        raise


class UpdateIncomeCashView(UpdateAPIView):
    """
    Представление изменяет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        income = self.get_object()

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested to update "
            f"income [ID: {income.pk}, "
            f"name: {income.categories.categoryName}]")

        try:
            response = super(UpdateIncomeCashView, self). \
                update(request, *args, **kwargs)
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully updated "
                f"income [ID: {income.pk}, "
                f"name: {income.categories.categoryName}].")
            return response

        except Exception as e:
            logger.error(
                f"Updating income [ID: {income.pk}, "
                f"name: {income.categories.categoryName}] "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class DeleteIncomeCashView(DestroyAPIView):
    """
    Представление удаляет сумму дохода в категории
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        income = self.get_object()

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested to delete "
            f"income [ID: {income.pk}, "
            f"name: {income.categories.categoryName}].")

        try:
            response = super(DeleteIncomeCashView, self). \
                delete(request, *args, **kwargs)
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully deleted "
                f"income [ID: {income.pk}, "
                f"name: {income.categories.categoryName}].")
            return response

        except Exception as e:
            logger.error(
                f"Deleting income [ID: {income.pk}, "
                f"name: {income.categories.categoryName}] "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class GetOutcomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested "
                f"a list of the 'Outcome' categories.")
            query_result = Categories.objects.filter(
                user_id=self.request.user.pk,
                income_outcome='outcome'
            )
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of the 'Outcome' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Outcome' categories "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


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
        return OutcomeCash.objects.filter(
            user_id=user_id,
            categories_id=category_id
        )

    def perform_create(self, serializer):
        category_name = Categories.objects.get(
            pk=self.request.data.get("category_id")).categoryName
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested to create '
                f'amount in outcome category [ID: '
                f'{self.request.data.get("category_id")}, '
                f'name: {category_name}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in outcome category '
                f'[ID: {self.request.data.get("category_id")}, '
                f'name: {category_name}] for user '
                f'[ID: {self.request.user.pk}, '
                f'name: {self.request.user}] failed with error: {e}.')
            raise

        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] successfully added '
            f'in outcome [ID: {saved_object.pk}, '
            f'amount: {saved_object.sum}] in category '
            f'[ID: {saved_object.categories.pk}, '
            f'name: {saved_object.categories.categoryName}].')


class Last5OutcomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей расходов
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested for "
            f"a list of 5 last Outcomes.")

        try:
            query_result = OutcomeCash.objects.filter(
                user_id=self.request.user.pk).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of 5 last Outcomes.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Outcomes "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class SumOutcomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех расходов по всем категориям
    """
    serializer_class = SumOutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested the amount "
            f"of all outcome in all categories.")

        try:
            query_result = OutcomeCash.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all outcome in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all outcome in all categories "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class SumOutcomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех расходов в разрезе категорий
    """
    serializer_class = SumOutcomeGroupCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested the amount "
            f"of all outcome in the context of categories.")

        try:
            query_result = OutcomeCash.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all outcome in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all outcome in the context "
                f"of categories for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class SumMonthlyOutcomeView(ListAPIView):
    """
    Представление возвращает сумму всех расходов пользователя
    в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumOutcomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return OutcomeCash.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all outcome in the context of categories '
            f'with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all outcome in the context '
                f'of categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all outcome in the context '
                f'of categories with a division by month '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
        raise


class SumPercentMonthlyOutcomeView(ListAPIView):
    """
    Представление возвращает сумму всех расходов пользователя
    в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentOutcomeGroupCashSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return OutcomeCash.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all outcome in the context of categories '
            f'with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all outcome in the context '
                f'of categories with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all outcome in the context '
                f'of categories with a division by month as '
                f'a percentage for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
        raise


class UpdateOutcomeCashView(UpdateAPIView):
    """
    Представление изменяет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        outcome = self.get_object()

        try:

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested to update '
                f'outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}].')

            response = super(UpdateOutcomeCashView, self). \
                update(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully updated '
                f'outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}].')

            return response

        except Exception as e:
            logger.error(
                f'Updating outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')


class DeleteOutcomeCashView(DestroyAPIView):
    """
    Представление удаляет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        outcome = self.get_object()

        try:

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested to delete '
                f'outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}].')

            response = super(DeleteOutcomeCashView, self). \
                delete(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully deleted '
                f'outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}].')

            return response

        except Exception as e:
            logger.error(
                f'Deleting outcome [ID: {outcome.pk}, '
                f'name: {outcome.categories.categoryName}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')


class GetMoneyBoxCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов с суммами и целями
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        money_box_cat = Categories.objects.filter(
            user_id=self.request.user.pk,
            income_outcome='money_box'
        )

        try:
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested "
                f"a list of the 'Accumulate' categories.")
            query_result = Response(
                money_box_cat.values(
                    'categoryName',
                    'category_type',
                    'income_outcome',
                    'user_id',
                    'is_hidden')
                .annotate(sum=Sum('moneybox__sum'),
                          target=F('moneybox__target'),
                          category_id=F('id')))
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of the 'Accumulate' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Accumulate' categories "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error {e}.")
            raise


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
        return MoneyBox.objects.filter(
            user_id=user_id,
            categories_id=category_id
        )

    def perform_create(self, serializer):
        category_name = Categories.objects.get(
            pk=self.request.data.get("category_id")).categoryName
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] requested '
                f'to create amount in accumulate category '
                f'[ID: {self.request.data.get("category_id")}, '
                f'name: {category_name}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in accumulate category '
                f'[ID: {self.request.data.get("category_id")}, '
                f'name: {category_name}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] failed with error: {e}.')
            raise

        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] successfully added '
            f'in accumulate [ID: {saved_object.pk}, '
            f'amount: {saved_object.sum}] in category '
            f'[ID: {saved_object.categories.pk}, '
            f'name: {saved_object.categories.categoryName}].')


class Last5MoneyBoxView(ListAPIView):
    """
    Представление возвращает 5 последних записей накоплений
    """
    serializer_class = MoneyBoxSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested for "
            f"a list of 5 last Accumulates.")

        try:
            query_result = MoneyBox.objects.filter(
                user_id=self.request.user.pk).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"a list of 5 last Accumulates.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Accumulates "
                f"for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class SumMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений по всем категориям
    """
    serializer_class = SumMoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested the amount "
            f"of all accumulate in all categories.")

        try:
            query_result = MoneyBox.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all accumulate in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all accumulate in "
                f"all categories for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] is filed with error: {e}.")
            raise


class SumMoneyBoxGroupView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений в разрезе категорий
    """
    serializer_class = SumMoneyBoxGroupSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested the amount "
            f"of all accumulate in the context of categories.")

        try:
            query_result = MoneyBox.objects.filter(
                user_id=self.request.user.pk).values('user').distinct()
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] successfully received "
                f"the amount of all accumulate in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all accumulate in "
                f"the context of categories for user "
                f"[ID: {self.request.user.pk}, name: {self.request.user}] "
                f"is filed with error: {e}.")
            raise


class SumMonthlyMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений пользователя
    в разрезе категорий с разделением по месяцам.
    """
    serializer_class = MonthlySumMoneyBoxGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MoneyBox.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all accumulate in the context of categories '
            f'with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all accumulate in the context '
                f'of categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all accumulate in the context '
                f'of categories with a division by month '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
        raise


class SumPercentMonthlyMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений пользователя
    в разрезе категорий с разделением по месяцам в процентах.
    """
    serializer_class = MonthlySumPercentMoneyBoxGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MoneyBox.objects.filter(user_id=self.request.user.pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            f'The user [ID: {self.request.user.pk}, '
            f'name: {self.request.user}] requested the amount '
            f'of all accumulate in the context of categories '
            f'with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully received '
                f'the amount of all accumulate in the context of categories '
                f'with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all accumulate in the context '
                f'of categories with a division by month as a percentage '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
        raise


class UpdateMoneyBoxView(UpdateAPIView):
    """
    Представление изменяет сумму накопления в категории
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        money_box = self.get_object()

        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] '
                f'requested to update accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}].')

            serializer = self.get_serializer(money_box, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(instance=money_box)

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] '
                f'successfully updated accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}].')

            return Response(serializer.data)

        except Exception as e:
            logger.error(
                f'Updating accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
            return Response({'error': str(e)}, status=400)


class DeleteMoneyBoxView(DestroyAPIView):
    """
    Представление удаляет сумму в накоплении
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        money_box = self.get_object()

        try:

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] '
                f'requested to delete accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}].')

            response = super(DeleteMoneyBoxView, self). \
                delete(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] '
                f'successfully deleted accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}].')

            return response

        except Exception as e:
            logger.error(
                f'Deleting accumulate [ID: {money_box.pk}, '
                f'name: {money_box.categories.categoryName}] '
                f'for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')


class BalanceAPIView(APIView):
    """
    Представление возвращает баланс пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            date_start = self.request.query_params.get('date_start')
            date_end = self.request.query_params.get('date_end')

            date_end = datetime.strptime(date_end, '%Y-%m-%d') \
                if date_end else datetime.now()
            date_start = datetime.strptime(date_start, '%Y-%m-%d') \
                if date_start else date_end - timedelta(days=365)

            logger.info(
                f"The user [ID: {self.request.user.pk}, name: "
                f"{self.request.user}] requested balance for date range "
                f"{date_start} to {date_end}.")

            income_sum = IncomeCash.objects.filter(
                user_id=self.request.user.pk,
                date__range=(date_start, date_end)). \
                             aggregate(Sum('sum')).get('sum__sum', 0.00) or 0
            outcome_sum = OutcomeCash.objects.filter(
                user_id=self.request.user.pk,
                date__range=(date_start, date_end)). \
                              aggregate(Sum('sum')).get('sum__sum', 0.00) or 0
            money_box_sum = MoneyBox.objects.filter(
                user_id=self.request.user.pk,
                date__range=(date_start, date_end)). \
                                aggregate(Sum('sum')).get('sum__sum', 0.00) or 0

            balance = round(income_sum - (outcome_sum + money_box_sum), 2)
            logger.info(
                f'The user [ID: {self.request.user.pk}, name: '
                f'{self.request.user}] successfully received their '
                f'balance for the period {date_start} - {date_end}.')
            return JsonResponse({'sum_balance': balance})

        except Exception as e:
            logger.exception(
                f"Requesting balance for user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] failed with error {e}.")
            return JsonResponse(
                {'error': 'An error occurred while processing the request'})


def date_filter(queryset, start_date=None, end_date=None):
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
        logger.info(f'Start date filter applied: {start_date}')
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
        logger.info(f'End date filter applied: {end_date}')
    return queryset


def parse_date(date_str, param_name):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        logger.exception(f"Incorrect date format for {param_name} for report")
        raise serializers.ValidationError(
            f'Incorrect date format for {param_name}, should be YYYY-MM-DD')


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
            date_start = parse_date(date_start, 'date_start')

        if date_end:
            date_end = parse_date(date_end, 'date_end')

        try:
            logger.info(
                f"The user [ID: {self.request.user.pk}, "
                f"name: {self.request.user}] requested report.")

            filters = {'user_id': self.request.user.pk}
            if date_start:
                filters['date__gte'] = date_start
            if date_end:
                filters['date__lte'] = date_end

            income_cash = IncomeCash.objects.filter(**filters). \
                order_by('-date')
            outcome_cash = OutcomeCash.objects.filter(**filters). \
                order_by('-date')
            money_box = MoneyBox.objects.filter(**filters).order_by('-date')

            queryset = {
                'income_cash': income_cash,
                'outcome_cash': outcome_cash,
                'money_box': money_box,
            }

            serializer = self.serializer_class(queryset,
                                               context={'request': request})
            logger.info(
                f'Report for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] successfully retrieved.')
            return Response(serializer.data)

        except Exception as e:
            logger.error(
                f'Requesting report for user [ID: {self.request.user.pk}, '
                f'name: {self.request.user}] is filed with error: {e}.')
