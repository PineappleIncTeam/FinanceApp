from rest_framework import serializers

from api.models import User, Categories, OutcomeCash, IncomeCash, MoneyBox


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined']

class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'password')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['categoryName', ]


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
