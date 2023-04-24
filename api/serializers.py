from django.db.models import Q
from django.db.models.aggregates import Sum
from rest_framework import serializers
from .models import Categories, OutcomeCash, IncomeCash, MoneyBox
from datetime import datetime
from .utils import MONTH_NAMES
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='pk', required=False)
    is_hidden = serializers.BooleanField(default=False)

    def create(self, validated_data):
        cat_name = validated_data.get('category_name')
        category_type = validated_data.get('category_type')
        income_outcome = validated_data.get('income_outcome')
        user_id = self.context.get('request').user.pk
        is_hidden = validated_data.get('is_hidden', False)

        category, created = Categories.objects.get_or_create(
            user_id=user_id,
            category_name=cat_name,
            category_type=category_type,
            income_outcome=income_outcome,
            is_hidden=is_hidden
        )
        if not created:
            raise serializers.ValidationError('Категория с таким названием уже существует')

        return category

    class Meta:
        model = Categories
        fields = ('category_name', 'category_id', 'category_type', 'income_outcome', 'user_id', 'is_hidden')


class MoneyBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBox
        fields = ('box_name', 'box_sum', 'user')


class IncomeCashSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    category_id = serializers.IntegerField(source='categories_id')
    category_name = serializers.CharField(source='categories.category_name', required=False)
    category_type = serializers.CharField(source='categories.category_type', required=False)
    sum = serializers.DecimalField(max_digits=19, decimal_places=2, required=False, default=0)
    date = serializers.SerializerMethodField()

    class Meta:
        model = IncomeCash
        fields = ('id', 'user', 'category_id', 'category_name', 'category_type', 'sum', 'date')

    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.get('categories_id')
        sum_value = validated_data.get('sum')
        date = validated_data.get('date')

        category = get_object_or_404(Categories, user_id=user_id, id=category_id)

        income_cash = IncomeCash.objects.create(
            user_id=user_id,
            category=category,
            sum=sum_value,
            date=date
        )
        return income_cash

    def get_date(self, validated_data):
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                  "Ноября", "Декабря"]
        try:
            today = datetime.strptime(validated_data.date, '%Y-%m-%d')
        except:
            today = validated_data.date
        num_week_day = datetime.weekday(today)
        num_month = int(datetime.strftime(today, '%m')) - 1
        return datetime.strftime(today, f'%d {months[num_month]} %Y, {days[num_week_day]}')


class SumIncomeCashSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')
    constant_sum = serializers.SerializerMethodField()
    once_sum = serializers.SerializerMethodField()

    def get_constant_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        constant_sum = IncomeCash.objects.filter(
            user_id=user_id,
            categories__category_type='constant',
            date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        return constant_sum

    def get_once_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        once_sum = IncomeCash.objects.filter(
            user_id=user_id,
            categories__category_type='once',
            date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        return once_sum

    class Meta:
        model = IncomeCash
        fields = ('user_id', 'constant_sum', 'once_sum')


class SumIncomeGroupCashSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    def get_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        once_sum = IncomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)).values('categories__category_name').annotate(
            result_sum=Sum('sum'))
        return once_sum

    class Meta:
        model = IncomeCash
        fields = ('sum',)


class OutcomeCashSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    category_id = serializers.IntegerField(source='categories_id')
    category_name = serializers.CharField(source='categories.category_name', required=False)
    category_type = serializers.CharField(source='categories.category_type', required=False)
    sum = serializers.DecimalField(max_digits=19, decimal_places=2, required=False, default=0)
    date = serializers.SerializerMethodField()

    class Meta:
        model = OutcomeCash
        fields = ('id', 'user', 'category_id', 'category_name', 'category_type', 'sum', 'date')

    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.get('categories_id')
        sum_value = validated_data.get('sum')
        date = validated_data.get('date')

        category = get_object_or_404(Categories, user_id=user_id, id=category_id)

        outcome_cash = OutcomeCash.objects.create(
            user_id=user_id,
            category=category,
            sum=sum_value,
            date=date
        )
        return outcome_cash

    def get_date(self, validated_data):
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                  "Ноября", "Декабря"]
        try:
            today = datetime.strptime(str(validated_data.date), '%Y-%m-%d')
        except:
            today = validated_data.date
        num_week_day = datetime.weekday(today)
        num_month = int(datetime.strftime(today, '%m')) - 1
        return datetime.strftime(today, f'%d {months[num_month]} %Y, {days[num_week_day]}')


class SumOutcomeCashSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')
    constant_sum = serializers.SerializerMethodField()
    once_sum = serializers.SerializerMethodField()

    def get_constant_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        constant_sum = OutcomeCash.objects.filter(
            user_id=user_id,
            categories__category_type='constant',
            date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        return constant_sum

    def get_once_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        once_sum = OutcomeCash.objects.filter(
            user_id=user_id,
            categories__category_type='once',
            date__range=(date_start, date_end)).aggregate(
            Sum('sum')).get('sum__sum', 0.00)
        return once_sum

    class Meta:
        model = OutcomeCash
        fields = ('user_id', 'constant_sum', 'once_sum')


class SumOutcomeGroupCashSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    def get_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'),
                                           '%Y-%m-%d').date()
            date_end = datetime.strptime(self.context.get('request').query_params.get('date_end'), '%Y-%m-%d').date()
        except:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        once_sum = OutcomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)).values('categories__category_name').annotate(
            result_sum=Sum('sum'))
        return once_sum

    class Meta:
        model = OutcomeCash
        fields = ('sum',)


class MonthlySumIncomeGroupCashSerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        user_id = self.context.get('request').user.pk
        date_start = self.context.get('request').query_params.get('date_start')
        date_end = self.context.get('request').query_params.get('date_end')
        if not date_start or not date_end:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        incomes = IncomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)
        ).values('categories__category_name', 'date').annotate(
            result_sum=Sum('sum')
        ).order_by('categories__category_name', 'date')

        categories = {}
        for income in incomes:
            month = MONTH_NAMES[income['date'].month]
            category_name = income['categories__category_name']
            if category_name not in categories:
                categories[category_name] = {}
            if month not in categories[category_name]:
                categories[category_name][month] = income['result_sum']
            else:
                categories[category_name][month] += income['result_sum']

        result = []
        for category_name, months in categories.items():
            category_dict = {}
            for month in self.get_requested_months(date_start, date_end):
                category_dict[month] = months.get(month, 0)
            result.append({category_name: category_dict})

        return result

    def get_requested_months(self, date_start, date_end):
        date_start_str = self.context.get('request').query_params.get('date_start')
        date_end_str = self.context.get('request').query_params.get('date_end')

        if date_start_str and date_end_str:
            date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
        else:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        months = []
        while date_start <= date_end:
            months.append(MONTH_NAMES[date_start.month])
            next_month = date_start.month + 1 if date_start.month < 12 else 1
            date_start = date_start.replace(year=date_start.year + 1 if next_month == 1 else date_start.year,
                                            month=next_month, day=1)
        return months

    class Meta:
        model = IncomeCash
        fields = ('sum',)


class MonthlySumOutcomeGroupCashSerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        user_id = self.context.get('request').user.pk
        date_start = self.context.get('request').query_params.get('date_start')
        date_end = self.context.get('request').query_params.get('date_end')
        if not date_start or not date_end:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        outcomes = OutcomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)
        ).values('categories__category_name', 'date').annotate(
            result_sum=Sum('sum')
        ).order_by('categories__category_name', 'date')

        categories = {}
        for outcome in outcomes:
            month = MONTH_NAMES[outcome['date'].month]
            category_name = outcome['categories__category_name']
            if category_name not in categories:
                categories[category_name] = {}
            if month not in categories[category_name]:
                categories[category_name][month] = outcome['result_sum']
            else:
                categories[category_name][month] += outcome['result_sum']

        result = []
        for category_name, months in categories.items():
            category_dict = {}
            for month in self.get_requested_months(date_start, date_end):
                category_dict[month] = months.get(month, 0)
            result.append({category_name: category_dict})

        return result

    def get_requested_months(self, date_start, date_end):
        date_start_str = self.context.get('request').query_params.get('date_start')
        date_end_str = self.context.get('request').query_params.get('date_end')

        if date_start_str and date_end_str:
            date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
        else:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        months = []
        while date_start <= date_end:
            months.append(MONTH_NAMES[date_start.month])
            next_month = date_start.month + 1 if date_start.month < 12 else 1
            date_start = date_start.replace(year=date_start.year + 1 if next_month == 1 else date_start.year,
                                            month=next_month, day=1)
        return months

    class Meta:
        model = OutcomeCash
        fields = ('sum',)


class MonthlySumPercentIncomeGroupCashSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        user_id = self.context.get('request').user.pk
        req_date_start = self.context.get('request').query_params.get('date_start')
        req_date_end = self.context.get('request').query_params.get('date_end')
        if not req_date_start or not req_date_end:
            date_start = IncomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = IncomeCash.objects.all().order_by('-date').values('date')[0].get('date')
        else:
            date_start = datetime.strptime(req_date_start, '%Y-%m-%d').date()
            date_end = datetime.strptime(req_date_end, '%Y-%m-%d').date()

        incomes = IncomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)
        ).values('date', 'categories__category_name').annotate(
            result_sum=Sum('sum')
        )

        categories = {}
        for income in incomes:
            month = MONTH_NAMES[income['date'].month]
            category_name = income['categories__category_name']
            if category_name not in categories:
                categories[category_name] = {}
            categories[category_name][month] = income['result_sum']

        requested_months = self.get_requested_months(date_start, date_end)
        total_by_month = {month: sum(data.get(month, 0) for data in categories.values()) for month in requested_months}
        for category in categories:
            for month, total in categories[category].items():
                categories[category][month] = round(total / total_by_month[month] * 100, 1) if total_by_month[
                                                                                                   month] != 0 else 0

        result = []
        for category_name, months in categories.items():
            category_dict = {}
            for month in requested_months:
                category_dict[month] = months.get(month, 0)
            result.append({category_name: category_dict})

        return result

    def get_requested_months(self, date_start, date_end):
        months = []
        while date_start <= date_end:
            months.append(MONTH_NAMES[date_start.month])
            next_month = date_start.month + 1 if date_start.month < 12 else 1
            date_start = date_start.replace(year=date_start.year + 1 if next_month == 1 else date_start.year,
                                            month=next_month, day=1)
        return months

    class Meta:
        model = IncomeCash
        fields = ('sum',)


class MonthlySumPercentOutcomeGroupCashSerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        user_id = self.context.get('request').user.pk
        date_start = self.context.get('request').query_params.get('date_start')
        date_end = self.context.get('request').query_params.get('date_end')
        if not date_start or not date_end:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        outcomes = OutcomeCash.objects.filter(
            Q(categories__category_type='once') | Q(categories__category_type='constant'),
            user_id=user_id,
            date__range=(date_start, date_end)
        ).values('date', 'categories__category_name').annotate(
            result_sum=Sum('sum')
        )

        categories = {}
        for outcome in outcomes:
            month = MONTH_NAMES[outcome['date'].month]
            category_name = outcome['categories__category_name']
            if category_name not in categories:
                categories[category_name] = {}
            categories[category_name][month] = outcome['result_sum']

        # расчёт процентов
        total_by_month = {month: sum(data.get(month, 0) for data in categories.values()) for month in
                          self.get_requested_months(date_start, date_end)}
        for category in categories:
            for month, total in categories[category].items():
                categories[category][month] = round(total / total_by_month[month] * 100, 1) if total_by_month[
                                                                                                   month] != 0 else 0

        result = []
        for category_name, months in categories.items():
            category_dict = {}
            for month in self.get_requested_months(date_start, date_end):
                category_dict[month] = months.get(month, 0)
            result.append({category_name: category_dict})

        return result

    def get_requested_months(self, date_start, date_end):
        date_start_str = self.context.get('request').query_params.get('date_start')
        date_end_str = self.context.get('request').query_params.get('date_end')

        if date_start_str and date_end_str:
            date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
        else:
            date_start = OutcomeCash.objects.all().order_by('date').values('date')[0].get('date')
            date_end = OutcomeCash.objects.all().order_by('-date').values('date')[0].get('date')

        months = []
        while date_start <= date_end:
            months.append(MONTH_NAMES[date_start.month])
            next_month = date_start.month + 1 if date_start.month < 12 else 1
            date_start = date_start.replace(year=date_start.year + 1 if next_month == 1 else date_start.year,
                                            month=next_month, day=1)
        return months

    class Meta:
        model = OutcomeCash
        fields = ('sum',)
