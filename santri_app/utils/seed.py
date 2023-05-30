from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
env_name = settings.ENV_NAME or None


if env_name == "local" and not User.objects.filter(email="admin@example.com").exists():
    print("-" * 8)
    print("Create local superuser")
    User.objects.create_superuser(email="admin@example.com", password="admin")
    print("Local super user created: login: admin@example.com, password: admin")
    print("-" * 8)
