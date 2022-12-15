# Generated by Django 4.1.3 on 2022-12-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_incomecash_date_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomecash',
            name='date',
            field=models.DateTimeField(verbose_name='Дата записи'),
        ),
        migrations.AlterField(
            model_name='incomecash',
            name='date_record',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='outcomecash',
            name='date',
            field=models.DateTimeField(verbose_name='Дата записи'),
        ),
        migrations.AlterField(
            model_name='outcomecash',
            name='date_record',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
    ]