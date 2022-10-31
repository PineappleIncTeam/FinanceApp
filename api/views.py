from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from .serializers import CategorySerializer, UserSerializer, CreateUserSerializer
from .models import Categories, User


# Create your views here.

class GetCreateCategoryAPIView(ListCreateAPIView):
    """
    Представление возвращает список всех категорий
    НУЖНО ПРОТЕСТИТЬ СОЗДАНИЕ КАТЕГОИЙ!!!
    """

    serializer_class = CategorySerializer
    queryset = Categories.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class CreateUser(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class GetUsers(ListAPIView):
    """
    Представление возвращает список всех пользователей
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()