from .serializers import CategorySerializer, IncomeCashSerializer
from .models import Categories, User, IncomeCash

from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated


class GetCreateCategoryAPIView(ListCreateAPIView):
    """
    Представление возвращает список всех категорий (GET)
    и создает новые категории (POST)
    Виды категорий (category_type):
        constant - постоянная
        once - разовая

    """

    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user_id = self.request.user.pk
        return Categories.objects.filter(user_id=user_id)


class DeleteCategory(DestroyAPIView):
    """
    Удаление категории (DELETE)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated,)

class UpdateCategory(UpdateAPIView):
    """
    Изменение категории (PUT)
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = (IsAuthenticated, )

class AddIncomeCash(ListCreateAPIView):
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.pk
        category_id = self.request.data.get('category_id')
        return IncomeCash.objects.filter(user_id=user_id, categories_id=category_id)

    def perform_create(self, serializer):
        serializer.save()

class Last5IncomeCash(ListAPIView):
    serializer_class = IncomeCashSerializer
    queryset = IncomeCash.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.pk
        return IncomeCash.objects.filter(user_id=user_id).order_by('-date')[:5]