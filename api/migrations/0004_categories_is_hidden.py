# Generated by Django 4.1.3 on 2023-04-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_incomecash_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]