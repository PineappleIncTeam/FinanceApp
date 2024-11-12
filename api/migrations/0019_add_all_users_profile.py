from django.db import migrations, utils


def load_data(apps, schema_editor):
    profile = apps.get_model('api', 'Profile')
    user = apps.get_model('api', 'User')

    users = user.objects.all()
    for us in users:
        profile.objects.get_or_create(user=us)





class Migration(migrations.Migration):
    dependencies = [
        ('api', '0018_alter_profile_country_alter_profile_first_name'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
