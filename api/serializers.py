from api.models import User, Categories, OutcomeCash, IncomeCash, MoneyBox

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class CategorySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cat_name = validated_data.__getitem__('categoryName')
        user_id = self.context.get('request').user.pk
        category = Categories.objects.create(user_id=user_id, categoryName=cat_name)
        return category

    class Meta:
        model = Categories
        fields = ['categoryName', 'user_id' ]


class OutcomeCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCash
        fields = ['reg_sum', 'var_sum', 'categories', 'date', 'user']


class IncomeCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCash
        fields = ['reg_sum', 'var_sum', 'categories', 'date', 'user']


class MoneyBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBox
        fields = ['box_name', 'box_sum', 'user']
