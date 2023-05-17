# Generated by Django 4.1.3 on 2023-05-10 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_alter_moneybox_box_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneybox',
            name='box_name',
        ),
        migrations.AddField(
            model_name='moneybox',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.categories', verbose_name='Категория'),
        ),
    ]
