from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import AbstractUser

"""
    Используем встроенную модель User
"""


class User(AbstractUser):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.last_login:
            Categories.objects.create(categoryName='Зарплата', user=self, category_type='constant')
            Categories.objects.create(categoryName='Подработка', user=self, category_type='constant')
            Categories.objects.create(categoryName='Пассивный доход', user=self, category_type='constant')
            Categories.objects.create(categoryName='Подработка', user=self, category_type='once')
            Categories.objects.create(categoryName='Наследство', user=self, category_type='once')
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

class Categories(models.Model):
    constant_cat = 'constant'
    once_cat = 'once'
    CAT_TYPES = [
        (constant_cat, 'Постоянные'),
        (once_cat, 'Разовые'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    categoryName = models.CharField(max_length=255, default="Название категории", verbose_name='Название категории')
    category_type = models.CharField(max_length=8, choices=CAT_TYPES, default=constant_cat)

    def __str__(self):
        return self.categoryName


class AbstractCash(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    constant_sum = models.DecimalField(max_digits=19, decimal_places=2,verbose_name='Постоянная сумма')
    once_sum = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Разовая сумма')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return str(self.categories) + str(self.date)

class OutcomeCash(AbstractCash):
    pass


class IncomeCash(AbstractCash):
    pass


class MoneyBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    box_name = models.CharField(max_length=255, verbose_name='Название копилки')
    box_sum = models.IntegerField(verbose_name='Сумма в копилке')
