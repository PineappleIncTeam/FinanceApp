from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import AbstractUser

"""
    Используем встроенную модель User
"""


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.last_login:
            # заполнение категорий доходов
            Category.objects.create(category_name='Зарплата', user=self, category_type='constant',
                                    income_outcome='income')
            Category.objects.create(category_name='Подработка', user=self, category_type='constant',
                                    income_outcome='income')
            Category.objects.create(category_name='Пассивный доход', user=self, category_type='constant',
                                    income_outcome='income')
            Category.objects.create(category_name='Подработка', user=self, category_type='once',
                                    income_outcome='income')
            Category.objects.create(category_name='Наследство', user=self, category_type='once',
                                    income_outcome='income')
            # заполнение категорий расходов
            Category.objects.create(category_name='Еда', user=self, category_type='constant',
                                    income_outcome='outcome')
            Category.objects.create(category_name='Одежда', user=self, category_type='constant',
                                    income_outcome='outcome')
            Category.objects.create(category_name='Развлечения', user=self, category_type='constant',
                                    income_outcome='outcome')
            Category.objects.create(category_name='ЖКХ', user=self, category_type='constant',
                                    income_outcome='outcome')
            Category.objects.create(category_name='Внезапная покупка', user=self, category_type='once',
                                    income_outcome='outcome')

        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class Category(models.Model):
    constant_cat = 'constant'  # постоянные
    once_cat = 'once'  # разовые
    CAT_TYPES = [
        (constant_cat, 'Постоянные'),
        (once_cat, 'Разовые'),
    ]

    income_cat = 'income'
    outcome_cat = 'outcome'

    CAT_INCOME_OUTCOME = [
        (income_cat, 'Категория доходов'),
        (outcome_cat, 'Категория расходов'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category_name = models.CharField(max_length=255, default="Название категории", verbose_name='Название категории',
                                     unique=True)
    category_type = models.CharField(max_length=8, choices=CAT_TYPES, default=constant_cat)
    income_outcome = models.CharField(max_length=11, choices=CAT_INCOME_OUTCOME, default=income_cat)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


class AbstractCash(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    sum = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Сумма')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 null=True, blank=True)
    date = models.DateField(verbose_name='Дата записи')
    date_record = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    def __str__(self):
        return f'{str(self.category)} {str(self.date)}'


class OutcomeCash(AbstractCash):
    pass


class IncomeCash(AbstractCash):
    pass


class MoneyBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    box_name = models.CharField(max_length=255, verbose_name='Название копилки')
    box_sum = models.IntegerField(verbose_name='Сумма в копилке')
