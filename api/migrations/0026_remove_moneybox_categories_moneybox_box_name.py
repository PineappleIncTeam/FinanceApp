# Generated by Django 4.1.3 on 2023-05-10 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_rename_category_moneybox_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneybox',
            name='categories',
        ),
        migrations.AddField(
            model_name='moneybox',
            name='box_name',
            field=models.CharField(default='Название накопления', verbose_name='Название накопления'),
        ),
    ]
