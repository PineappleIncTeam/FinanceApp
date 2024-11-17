from django.db import migrations
import json
import os


def load_data(apps, schema_editor):
    countries = apps.get_model('api', 'Country')

    file_path = os.path.join(os.path.dirname(__file__), 'data/oksm.json')

    with open(file_path, encoding="utf8") as f:
        data = json.load(f)

        country_objects = [
            countries(name=item.get("name"), code=item.get("alfa2"))
            for item in data
        ]
        countries.objects.bulk_create(country_objects, batch_size=1000)


def reverse_table_population(apps, schema_editor) -> None:
    """Reverse table population."""
    country = apps.get_model('api', 'Country')
    countries = country.objects.all()
    countries.delete()

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0014_country_profile'),
    ]

    operations = [
        migrations.RunPython(load_data, reverse_table_population),
    ]
