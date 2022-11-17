from .models import User, Categories, OutcomeCash, IncomeCash, MoneyBox

from rest_framework import serializers


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
        fields = ['reg_sum', 'var_sum', 'categories', 'date', 'user']


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
    reg_sum = serializers.IntegerField(required=False)
    var_sum = serializers.IntegerField(required=False)
    class Meta:
        model = IncomeCash
        fields = ('user', 'category_id', 'categoryName', 'category_type', 'reg_sum', 'var_sum', 'date')
    def create(self, validated_data):
        user_id = self.context.get('request').user.pk
        category_id = validated_data.__getitem__('categories_id')
        reg_sum = validated_data.__getitem__('reg_sum')
        var_sum = validated_data.__getitem__('var_sum')

        incomecash = IncomeCash.objects.create(
            user_id=user_id,
            categories_id=category_id,
            reg_sum=reg_sum,
            var_sum=var_sum)
        return incomecash