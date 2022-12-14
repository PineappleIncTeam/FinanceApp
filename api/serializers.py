from django.db.models.aggregates import Sum
from rest_framework import serializers
from .models import User, Categories, OutcomeCash, IncomeCash, MoneyBox
from django.http import JsonResponse
from datetime import datetime, date


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


# class CreateUserSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='pk', required=False)

    def create(self, validated_data):
        cat_name = validated_data.__getitem__('categoryName')
        category_type = validated_data.__getitem__('category_type')
        income_outcome = validated_data.__getitem__('income_outcome')
        user_id = self.context.get('request').user.pk
        category = Categories.objects.create(
            user_id=user_id,
            categoryName=cat_name,
            category_type=category_type,
            income_outcome=income_outcome)
        return category

    class Meta:
        model = Categories
        fields = ['categoryName', 'category_id', 'category_type', 'income_outcome', 'user_id']


# class OutcomeCashSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OutcomeCash
#         fields = ['constant_sum', 'once_sum', 'categories', 'date', 'user']


class MoneyBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBox
        fields = ['box_name', 'box_sum', 'user']


class IncomeCashSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    category_id = serializers.IntegerField(source='categories_id')
    categoryName = serializers.CharField(source='categories.categoryName', required=False)
    category_type = serializers.CharField(source='categories.category_type', required=False)
    sum = serializers.DecimalField(max_digits=19, decimal_places=2, required=False, default=0)
    # date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S, %a', required=False)
    date = serializers.SerializerMethodField()

    class Meta:
        model = IncomeCash
        fields = ('id', 'user', 'category_id', 'categoryName', 'category_type', 'sum', 'date')

    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.__getitem__('categories_id')
        sum = self.validated_data.__getitem__('sum')
        date = self.initial_data.get('date')

        # try:
        Categories.objects.get(user_id=user_id, id=category_id)

        incomecash = IncomeCash.objects.create(
            user_id=user_id,
            categories_id=category_id,
            sum=sum,
            date=date)
        return incomecash
        # except:
        #     raise ValueError(f"У пользователя с id {user_id} нет категории с id {category_id}")

    def get_date(self, validated_data):
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        monthes = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                   "Ноября", "Декабря"]
        try:
            today = datetime.strptime(validated_data.date, '%Y-%m-%d')
        except:
            today = validated_data.date
        num_week_day = datetime.weekday(today)
        num_month = int(datetime.strftime(today, '%m')) - 1
        return datetime.strftime(today, f'%d {monthes[num_month]} %Y, {days[num_week_day]}')


class SumIncomeCashSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')
    constant_sum = serializers.SerializerMethodField()
    once_sum = serializers.SerializerMethodField()

    def get_constant_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'), '%Y-%m-%d').date()
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
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'), '%Y-%m-%d').date()
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


class OutcomeCashSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    category_id = serializers.IntegerField(source='categories_id')
    categoryName = serializers.CharField(source='categories.categoryName', required=False)
    category_type = serializers.CharField(source='categories.category_type', required=False)
    sum = serializers.DecimalField(max_digits=19, decimal_places=2, required=False, default=0)
    # date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S, %a', required=False)
    date = serializers.SerializerMethodField()

    class Meta:
        model = OutcomeCash
        fields = ('id', 'user', 'category_id', 'categoryName', 'category_type', 'sum', 'date')

    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.__getitem__('categories_id')
        sum = self.validated_data.__getitem__('sum')
        date = self.initial_data.get('date')

        Categories.objects.get(user_id=user_id, id=category_id)

        outcomecash = OutcomeCash.objects.create(
            user_id=user_id,
            categories_id=category_id,
            sum=sum,
            date=date)
        return outcomecash


    def get_date(self, validated_data):
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        monthes = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                   "Ноября", "Декабря"]
        try:
            today = datetime.strptime(str(validated_data.date), '%Y-%m-%d')
        except:
            today = validated_data.date
        num_week_day = datetime.weekday(today)
        num_month = int(datetime.strftime(today, '%m')) - 1
        return datetime.strftime(today, f'%d {monthes[num_month]} %Y, {days[num_week_day]}')


class SumOutcomeCashSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')
    constant_sum = serializers.SerializerMethodField()
    once_sum = serializers.SerializerMethodField()

    def get_constant_sum(self, validated_data):
        user_id = self.context.get('request').user.pk
        try:
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'), '%Y-%m-%d').date()
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
            date_start = datetime.strptime(self.context.get('request').query_params.get('date_start'), '%Y-%m-%d').date()
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


