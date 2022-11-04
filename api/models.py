from django.db import models
from django.contrib.auth.models import AbstractUser

"""
    Используем встроенную модель User
"""


class User(AbstractUser):
    pass


class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    categoryName = models.CharField(max_length=255, default="Название категории", verbose_name='Название категории')

    def __str__(self):
        return self.categoryName


class AbstractCash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    reg_sum = models.IntegerField(verbose_name='Постоянная сумма')
    var_sum = models.IntegerField(verbose_name='Переменная сумма')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')


class OutcomeCash(AbstractCash):
    pass


class IncomeCash(AbstractCash):
    pass


class MoneyBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    box_name = models.CharField(max_length=255, verbose_name='Название копилки')
    box_sum = models.IntegerField(verbose_name='Сумма в копилке')
