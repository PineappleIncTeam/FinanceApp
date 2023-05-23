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
            Categories.objects.create(categoryName='Зарплата', user=self, category_type='constant',
                                      income_outcome='income')
            Categories.objects.create(categoryName='Подработка', user=self, category_type='constant',
                                      income_outcome='income')
            Categories.objects.create(categoryName='Пассивный доход', user=self, category_type='constant',
                                      income_outcome='income')
            Categories.objects.create(categoryName='Подработка', user=self, category_type='once',
                                      income_outcome='income')
            Categories.objects.create(categoryName='Наследство', user=self, category_type='once',
                                      income_outcome='income')
            # заполнение категорий расходов
            Categories.objects.create(categoryName='Еда', user=self, category_type='constant',
                                      income_outcome='outcome')
            Categories.objects.create(categoryName='Одежда', user=self, category_type='constant',
                                      income_outcome='outcome')
            Categories.objects.create(categoryName='Развлечения', user=self, category_type='constant',
                                      income_outcome='outcome')
            Categories.objects.create(categoryName='ЖКХ', user=self, category_type='constant',
                                      income_outcome='outcome')
            Categories.objects.create(categoryName='Внезапная покупка', user=self, category_type='once',
                                      income_outcome='outcome')

        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class Categories(models.Model):
    constant_cat = 'constant'  # постоянные
    once_cat = 'once'  # разовые
    accum_cat = 'accumulate'  # накопления
    CAT_TYPES = [
        (constant_cat, 'Постоянные'),
        (once_cat, 'Разовые'),
        (accum_cat, 'Накопления')
    ]

    income_cat = 'income'
    outcome_cat = 'outcome'

    CAT_INCOME_OUTCOME = [
        (income_cat, 'Категория доходов'),
        (outcome_cat, 'Категория расходов'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    categoryName = models.CharField(max_length=255, default="Название категории", verbose_name='Название категории')
    category_type = models.CharField(max_length=10, choices=CAT_TYPES, default=constant_cat)
    income_outcome = models.CharField(max_length=11, choices=CAT_INCOME_OUTCOME, default=income_cat)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.categoryName


class AbstractCash(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    sum = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Сумма')
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, verbose_name='Категория', null=True)
    date = models.DateField(verbose_name='Дата записи')
    date_record = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    def __str__(self):
        return f'{str(self.categories)} {str(self.date)}'


class OutcomeCash(AbstractCash):
    pass


class IncomeCash(AbstractCash):
    pass


class MoneyBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория', null=True)
    box_sum = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Сумма накопления')
    box_target = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Конечная цель')
    date = models.DateField(verbose_name='Дата создания накопления')

    def save(self, *args, **kwargs):
        # Создаём запись в MoneyBox
        try:
            prev_box_sum = MoneyBox.objects.get(pk=self.pk).box_sum
        except MoneyBox.DoesNotExist:
            prev_box_sum = 0
        # Одновременно создаём запись в OutcomeCash
        OutcomeCash.objects.create(user=self.user, sum=self.box_sum - prev_box_sum, categories=self.categories,
                                   date=self.date)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        outcome_cash = OutcomeCash.objects.filter(user=self.user, categories=self.categories)
        if outcome_cash:
            outcome_cash.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f'{self.categories} {self.box_sum} {self.box_target}'
