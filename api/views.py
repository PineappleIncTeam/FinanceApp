from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id)

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