# Generated by Django 4.2.1 on 2024-10-19 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countries',
            name='full_name',
            field=models.CharField(max_length=146, verbose_name='Полное название'),
        ),
    ]
