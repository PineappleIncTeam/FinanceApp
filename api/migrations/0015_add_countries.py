from django.db import migrations
import json
import os


def load_data(apps, schema_editor):
    countries = apps.get_model('api', 'Country')

    # Путь к файлу с данными
    file_path = os.path.join(os.path.dirname(__file__), 'data/oksm.json')

    with open(file_path, encoding="utf8") as f:
        data = json.load(f)
        for item in data:
            country = {"name": item.get("name"), "code": item.get("alfa2")}
            countries.objects.create(**country)



class Migration(migrations.Migration):
    dependencies = [
        ('api', '0014_country_profile'),  # Замените на имя предыдущей миграции
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
