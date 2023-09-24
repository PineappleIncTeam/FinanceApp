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
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] created category {serializer.instance}')

    def get_queryset(self):
        user_id = self.request.user.pk

        try:
            logger.info(
                f'The user [ID: {user_id}, name: {self.request.user}] requested a list of all categories')
            query_result = Categories.objects.filter(user_id=user_id)
            logger.info(
                f'The user [ID: {user_id}, name: {self.request.user}] successfully received a list of all categories')
            return query_result

        except Exception as e:
            logger.error(
                f'Request a list of all categories for user [ID: {user_id}, name: {self.request.user}] is filed with error: {e}')
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
        user = request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
            'category_id': category.pk,
            'category_name': category.categoryName,
        }

        try:
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested to update category [ID: {log_context['category_id']}, name: {log_context['category_name']}].")

            response = super().update(request, *args, **kwargs)

            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully updated category [ID: {log_context['category_id']}, name: {log_context['category_name']}].")
            return response

        except Exception as e:
            logger.error(
                f"Updating category [ID: {log_context['category_id']}, name: {log_context['category_name']}] for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] failed with error: {e}.")
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
        user = request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
            'category_id': category.pk,
            'category_name': category.categoryName,
        }

        try:

            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested to delete category [ID: {log_context['category_id']}, name: {log_context['category_name']}]")

            response = super(DeleteCategoryView, self).delete(request, *args, **kwargs)

            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully deleted category [ID: {log_context['category_id']}, name: {log_context['category_name']}].")

            return response

        except Exception as e:
            logger.error(
                f"Deleting category [ID: {log_context['category_id']}, name: {log_context['category_name']}] for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}.")
            raise


class GetIncomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий доходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
        }

        try:
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested a list of the 'Income' categories.")
            query_result = Categories.objects.filter(user_id=log_context['user_id'],
                                                     income_outcome='income')
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of the 'Income' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Income' categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
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
        return IncomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested to create amount in income category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in income category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}] for user [ID: {self.request.user.pk}, name: {self.request.user}] failed with error: {e}.')
            raise

        category_id = saved_object.categories.pk
        category_name = saved_object.categories.categoryName

        income_id = saved_object.pk
        income_sum = saved_object.sum

        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully added in income [ID: {income_id}, amount: {income_sum}] in category [ID: {category_id}, name: {category_name}].')


class Last5IncomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей доходов
    """
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested for a list of 5 last Incomes")

        try:
            quesry_result = IncomeCash.objects.filter(user_id=user_id).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of 5 last Incomes.")
            return quesry_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Incomes for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


class SumIncomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех доходов по всем категориям
    """
    serializer_class = SumIncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all income in all categories.")

        try:
            query_result = IncomeCash.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all income in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all income in all categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


class SumIncomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех доходов в разрезе категорий
    """
    serializer_class = SumIncomeGroupCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all income in the context of categories.")

        try:
            query_result = IncomeCash.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all income in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all income in the context of categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all income in the context of categories with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all income in the context of categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all income in the context of categories with a division by month for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}')
        raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all income in the context of categories with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all income in the context of categories with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all income in the context of categories with a division by month as a percentage for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}')
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
        user = request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
            'income_id': income.pk,
            'income_name': income.categories.categoryName,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested to update income [ID: {log_context['user_id']}, name: {log_context['income_name']}]")

        try:
            response = super(UpdateIncomeCashView, self).update(request, *args, **kwargs)
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully updated income [ID: {log_context['user_id']}, name: {log_context['income_name']}].")
            return response

        except Exception as e:
            logger.error(
                f"Updating income [ID: {log_context['user_id']}, name: {log_context['income_name']}] for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}.")
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
        user = request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
            'income_id': income.pk,
            'income_name': income.categories.categoryName,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested to delete income [ID: {log_context['user_id']}, name: {log_context['income_name']}]")

        try:
            response = super(DeleteIncomeCashView, self).delete(request, *args, **kwargs)
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully deleted income [ID: {log_context['user_id']}, name: {log_context['income_name']}].")
            return response

        except Exception as e:
            logger.error(
                f"Deleting income [ID: {log_context['user_id']}, name: {log_context['income_name']}] for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}.")
            raise


class GetOutcomeCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
        }

        try:
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested a list of the 'Outcome' categories.")
            query_result = Categories.objects.filter(user_id=log_context['user_id'],
                                                     income_outcome='outcome')
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of the 'Outcome' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Outcome' categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
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
        return OutcomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested to create amount in outcome category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in outcome category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}] for user [ID: {self.request.user.pk}, name: {self.request.user}] failed with error: {e}.')
            raise

        category_id = saved_object.categories.pk
        category_name = saved_object.categories.categoryName

        outcome_id = saved_object.pk
        outcome_sum = saved_object.sum

        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully added in outcome [ID: {outcome_id}, amount: {outcome_sum}] in category [ID: {category_id}, name: {category_name}].')


class Last5OutcomeCashView(ListAPIView):
    """
    Представление возвращает 5 последних записей расходов
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested for a list of 5 last Outcomes.")

        try:
            query_result = OutcomeCash.objects.filter(user_id=user_id).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of 5 last Outcomes.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Outcomes for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}.")
            raise


class SumOutcomeCashView(ListAPIView):
    """
    Представление возвращает сумму всех расходов по всем категориям
    """
    serializer_class = SumOutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all outcome in all categories.")

        try:
            query_result = OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all outcome in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all outcome in all categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


class SumOutcomeCashGroupView(ListAPIView):
    """
    Представление возвращает сумму всех расходов в разрезе категорий
    """
    serializer_class = SumOutcomeGroupCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all outcome in the context of categories.")

        try:
            query_result = OutcomeCash.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all outcome in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all outcome in the context of categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all outcome in the context of categories with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all outcome in the context of categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all outcome in the context of categories with a division by month for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}.')
        raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all outcome in the context of categories with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all outcome in the context of categories with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all outcome in the context of categories with a division by month as a percentage for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}.')
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

        user_id = request.user.pk
        user_name = request.user.username

        outcome_id = outcome.pk
        outcome_name = outcome.categories.categoryName

        try:

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] requested to update outcome [ID: {outcome_id}, name: {outcome_name}]')

            response = super(UpdateOutcomeCashView, self).update(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] successfully updated outcome [ID: {outcome_id}, name: {outcome_name}].')

            return response

        except Exception as e:
            logger.error(
                f'Updating outcome [ID: {outcome_id}, name: {outcome_name}] for user [ID: {user_id}, name: {user_name}] is filed with error: {e}.')


class DeleteOutcomeCashView(DestroyAPIView):
    """
    Представление удаляет сумму расхода в категории
    """
    serializer_class = OutcomeCashSerializer
    queryset = OutcomeCash.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        outcome = self.get_object()

        user_id = request.user.pk
        user_name = request.user.username

        outcome_id = outcome.pk
        outcome_name = outcome.categories.categoryName

        try:

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] requested to delete outcome [ID: {outcome_id}, name: {outcome_name}].')

            response = super(DeleteOutcomeCashView, self).delete(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] successfully deleted outcome [ID: {outcome_id}, name: {outcome_name}].')

            return response

        except Exception as e:
            logger.error(
                f'Deleting outcome [ID: {outcome_id}, name: {outcome_name}] for user [ID: {user_id}, name: {user_name}] is filed with error: {e}.')


class GetMoneyBoxCategoriesView(ListAPIView):
    """
    Представление возвращает список категорий расходов с суммами и целями
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        money_box_cat = Categories.objects.filter(user_id=user.pk, income_outcome='money_box')

        log_context = {
            'user_id': user.pk,
            'user_name': user.username,
        }

        try:
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested a list of the 'Accumulate' categories.")
            query_result = Response(
                money_box_cat.values('categoryName', 'category_type', 'income_outcome', 'user_id', 'is_hidden')
                .annotate(sum=Sum('moneybox__sum'), target=F('moneybox__target'), category_id=F('id')))
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of the 'Accumulate' categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request a list of the 'Accumulate' categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error {e}.")
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
        return MoneyBox.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        try:
            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested to create amount in accumulate category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}].')
            saved_object = serializer.save()
        except Exception as e:
            logger.error(
                f'Creating amount in accumulate category [ID: {self.request.data.get("category_id")}, name: {Categories.objects.get(pk=self.request.data.get("category_id")).categoryName}] for user [ID: {self.request.user.pk}, name: {self.request.user}] failed with error: {e}.')
            raise

        category_id = saved_object.categories.pk
        category_name = saved_object.categories.categoryName

        money_box_id = saved_object.pk
        money_box_sum = saved_object.sum

        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully added in accumulate [ID: {money_box_id}, amount: {money_box_sum}] in category [ID: {category_id}, name: {category_name}].')


class Last5MoneyBoxView(ListAPIView):
    """
    Представление возвращает 5 последних записей накоплений
    """
    serializer_class = MoneyBoxSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested for a list of 5 last Accumulates.")

        try:
            query_result = MoneyBox.objects.filter(user_id=user_id).order_by('-date_record')[:5]
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received a list of 5 last Accumulates.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request for a list of 5 last Accumulates for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}.")
            raise


class SumMoneyBoxView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений по всем категориям
    """
    serializer_class = SumMoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all accumulate in all categories.")

        try:
            query_result = MoneyBox.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all accumulate in all categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all accumulate in all categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


class SumMoneyBoxGroupView(ListAPIView):
    """
    Представление возвращает сумму всех накоплений в разрезе категорий
    """
    serializer_class = SumMoneyBoxGroupSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        log_context = {
            'user_id': user_id,
            'user_name': self.request.user,
        }

        logger.info(
            f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] requested the amount of all accumulate in the context of categories.")

        try:
            query_result = MoneyBox.objects.filter(user_id=user_id).values('user').distinct()
            logger.info(
                f"The user [ID: {log_context['user_id']}, name: {log_context['user_name']}] successfully received the amount of all accumulate in the context of categories.")
            return query_result

        except Exception as e:
            logger.error(
                f"Request the amount of all accumulate in the context of categories for user [ID: {log_context['user_id']}, name: {log_context['user_name']}] is filed with error: {e}")
            raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all accumulate in the context of categories with a division by month.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all accumulate in the context of categories with a division by month.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all accumulate in the context of categories with a division by month for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}.')
        raise


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
        logger.info(
            f'The user [ID: {self.request.user.pk}, name: {self.request.user}] requested the amount of all accumulate in the context of categories with a division by month as a percentage.')
        try:
            if serializer.data:
                response = Response(serializer.data[0])
            else:
                response = Response([])

            logger.info(
                f'The user [ID: {self.request.user.pk}, name: {self.request.user}] successfully received the amount of all accumulate in the context of categories with a division by month as a percentage.')

            return response

        except Exception as e:
            logger.error(
                f'Request the amount of all accumulate in the context of categories with a division by month as a percentage for user [ID: {self.request.user.pk}, name: {self.request.user}] is filed with error: {e}.')
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

        user_id = request.user.pk
        user_name = request.user.username

        money_box_id = money_box.pk
        money_box_name = money_box.categories.categoryName

        try:

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] requested to update accumulate [ID: {money_box_id}, name: {money_box_name}]')

            response = super(UpdateMoneyBoxView, self).update(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] successfully updated accumulate [ID: {money_box_id}, name: {money_box_name}].')

            return response

        except Exception as e:
            logger.error(
                f'Updating accumulate [ID: {money_box_id}, name: {money_box_name}] for user [ID: {user_id}, name: {user_name}] is filed with error: {e}.')


class DeleteMoneyBoxView(DestroyAPIView):
    """
    Представление удаляет сумму в накоплении
    """
    serializer_class = MoneyBoxSerializer
    queryset = MoneyBox.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        money_box = self.get_object()

        user_id = request.user.pk
        user_name = request.user.username

        money_box_id = money_box.pk
        money_box_name = money_box.categories.categoryName

        try:

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] requested to delete accumulate [ID: {money_box_id}, name: {money_box_name}].')

            response = super(DeleteMoneyBoxView, self).delete(request, *args, **kwargs)

            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] successfully deleted accumulate [ID: {money_box_id}, name: {money_box_name}].')

            return response

        except Exception as e:
            logger.error(
                f'Deleting accumulate [ID: {money_box_id}, name: {money_box_name}] for user [ID: {user_id}, name: {user_name}] is filed with error: {e}.')


class BalanceAPIView(APIView):
    """
    Представление возвращает баланс пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.pk
        user_name = request.user.username

        try:
            date_start = self.request.query_params.get('date_start')
            date_end = self.request.query_params.get('date_end')

            date_end = datetime.strptime(date_end, '%Y-%m-%d') if date_end else datetime.now()
            date_start = datetime.strptime(date_start, '%Y-%m-%d') if date_start else date_end - timedelta(days=365)

            logger.info(
                f"The user [ID: {user_id}, name: {user_name}] requested balance for date range {date_start} to {date_end}")

            income_sum = IncomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
                Sum('sum')).get('sum__sum', 0.00)
            outcome_sum = OutcomeCash.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
                Sum('sum')).get('sum__sum', 0.00)
            money_box_sum = MoneyBox.objects.filter(user_id=user_id, date__range=(date_start, date_end)).aggregate(
                Sum('sum')).get('sum__sum', 0.00)

            balance = round(income_sum - (outcome_sum + money_box_sum), 2)
            logger.info(
                f'The user [ID: {user_id}, name: {user_name}] successfully received their balance for the period {date_start} - {date_end}')
            return JsonResponse({'sum_balance': balance})

        except Exception as e:
            logger.exception(f"Requesting balance for user [ID: {user_id}, name: {user_name}] failed with error {e}.")
            return JsonResponse({'error': 'An error occurred while processing the request'})


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
        raise serializers.ValidationError(f'Incorrect date format for {param_name}, should be YYYY-MM-DD')


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

        user_id = request.user.pk
        user_name = request.user.username

        try:
            logger.info(
                f"The user [ID: {user_id}, name: {user_name}] requested report.")

            filters = {'user_id': user_id}
            if date_start:
                filters['date__gte'] = date_start
            if date_end:
                filters['date__lte'] = date_end

            income_cash = IncomeCash.objects.filter(**filters).order_by('-date')
            outcome_cash = OutcomeCash.objects.filter(**filters).order_by('-date')
            money_box = MoneyBox.objects.filter(**filters).order_by('-date')

            queryset = {
                'income_cash': income_cash,
                'outcome_cash': outcome_cash,
                'money_box': money_box,
            }

            serializer = self.serializer_class(queryset, context={'request': request})
            logger.info(f'Report for user [ID: {user_id}, name: {user_name}] successfully retrieved.')
            return Response(serializer.data)

        except Exception as e:
            logger.error(
                f'Requesting report for user [ID: {user_id}, name: {user_name}] is filed with error: {e}.')
