# Generated by Django 4.1.3 on 2023-04-24 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_categories_is_hidden'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='incomecash',
            old_name='categories',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='outcomecash',
            old_name='categories',
            new_name='category',
        ),
    ]
