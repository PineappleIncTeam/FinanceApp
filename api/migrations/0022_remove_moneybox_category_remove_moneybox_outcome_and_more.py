# Generated by Django 4.1.3 on 2023-05-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_moneybox_outcome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneybox',
            name='category',
        ),
        migrations.RemoveField(
            model_name='moneybox',
            name='outcome',
        ),
        migrations.AddField(
            model_name='moneybox',
            name='box_name',
            field=models.CharField(default='Название накопления', verbose_name='Название накопления'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_type',
            field=models.CharField(choices=[('constant', 'Постоянные'), ('once', 'Разовые')], default='constant', max_length=10),
        ),
        migrations.AlterField(
            model_name='moneybox',
            name='box_target',
            field=models.IntegerField(verbose_name='Конечная цель'),
        ),
    ]
