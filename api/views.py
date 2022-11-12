from .serializers import CategorySerializer
from .models import Categories, User

from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated


class GetCreateCategoryAPIView(ListCreateAPIView):
    """
    Представление возвращает список всех категорий (GET)
    и создает новые категории (POST)

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


# class GetUsers(ListAPIView):
#     """
#     Представление возвращает список всех пользователей
#     """
#     serializer_class = UserSerializer
#     queryset = User.objects.all()