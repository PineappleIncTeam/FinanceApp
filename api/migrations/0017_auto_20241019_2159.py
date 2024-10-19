from django.db import migrations
import json
import os


def load_data(apps, schema_editor):
    countries = apps.get_model('api', 'Countries')

    # Путь к файлу с данными
    file_path = os.path.join(os.path.dirname(__file__), 'data/oksm.json')

    with open(file_path, encoding="utf8") as f:
        data = json.load(f)
        for item in data:
            item.pop("alfa2")
            item.pop("alfa3")
            countries.objects.create(**item)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0016_alter_countries_name'),  # Замените на имя предыдущей миграции
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
