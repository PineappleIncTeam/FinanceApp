# Generated by Django 4.1.3 on 2023-05-10 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_remove_moneybox_categories_moneybox_box_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category_type',
            field=models.CharField(choices=[('constant', 'Постоянные'), ('once', 'Разовые')], default='constant', max_length=10),
        ),
        migrations.AlterField(
            model_name='moneybox',
            name='box_sum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.outcomecash', verbose_name='Сумма накопления'),
        ),
    ]