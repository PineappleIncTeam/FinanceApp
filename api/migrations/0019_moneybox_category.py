# Generated by Django 4.1.3 on 2023-05-09 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_remove_moneybox_category_moneybox_outcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneybox',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.categories', verbose_name='Название накопления'),
        ),
    ]
