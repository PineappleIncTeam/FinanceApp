from django.db.models.aggregates import Sum
from rest_framework import serializers
from .models import User, Categories, OutcomeCash, IncomeCash, MoneyBox




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
        user_id = self.context.get('request').user.pk
        category = Categories.objects.create(
            user_id=user_id,
            categoryName=cat_name,
            category_type=category_type)
        return category

    class Meta:
        model = Categories
        fields = ['categoryName', 'category_id', 'category_type', 'user_id' ]


class OutcomeCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCash
        fields = ['constant_sum', 'once_sum', 'categories', 'date', 'user']


# class IncomeCashSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IncomeCash
#         fields = ['reg_sum', 'var_sum', 'categories', 'date', 'user']


class MoneyBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBox
        fields = ['box_name', 'box_sum', 'user']

class IncomeCashSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    category_id = serializers.IntegerField(source='categories_id')
    categoryName = serializers.CharField(source='categories.categoryName', required=False)
    category_type = serializers.CharField(source='categories.category_type', required=False)
    constant_sum = serializers.DecimalField(max_digits=19, decimal_places=2 ,required=False)
    once_sum = serializers.DecimalField(max_digits=19, decimal_places=2, required=False)
    class Meta:
        model = IncomeCash
        fields = ('user', 'category_id', 'categoryName', 'category_type', 'constant_sum', 'once_sum', 'date')
    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.__getitem__('categories_id')
        constant_sum = validated_data.__getitem__('constant_sum')
        once_sum = validated_data.__getitem__('once_sum')

        incomecash = IncomeCash.objects.create(
            user_id=user_id,
            categories_id=category_id,
            constant_sum=constant_sum,
            once_sum=once_sum)
        return incomecash

class SumIncomeCashSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')
    SUM_Constant_sum = serializers.SerializerMethodField()
    SUM_Once_sum = serializers.SerializerMethodField()

    def get_SUM_Constant_sum(self,validated_data):
        user_id = self.context.get('request').user.pk
        SUM_Constant_sum = IncomeCash.objects.filter(user_id=user_id).aggregate(Sum('constant_sum')).get('constant_sum__sum', 0.00)
        return SUM_Constant_sum

    def get_SUM_Once_sum(self,validated_data):
        user_id = self.context.get('request').user.pk
        SUM_Once_sum = IncomeCash.objects.filter(user_id=user_id).aggregate(Sum('once_sum')).get('once_sum__sum',0.00)
        return SUM_Once_sum

    class Meta:
        model = IncomeCash
        fields = ('user_id','SUM_Constant_sum', 'SUM_Once_sum')

