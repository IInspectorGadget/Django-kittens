from django.db import migrations
from django.contrib.auth.models import User

def create_new_user(apps, schema_editor):
    # Создаем нового пользователя
    User = apps.get_model('auth', 'User')
    User.objects.create_user(
        username='user1',
        password='user1',
        email='user1@user1.com',
        first_name='user1',
        last_name='user1'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('kittens', '0002_auto_20241001_1528'),
    ]

    operations = [
        migrations.RunPython(create_new_user),
    ]
