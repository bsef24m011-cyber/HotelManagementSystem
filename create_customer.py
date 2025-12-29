import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_project.settings")
django.setup()

from apps.users.models import User

def create_customer():
    username = "customer1"
    password = "password123"
    email = "customer1@example.com"
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role='CUSTOMER'
        )
        print(f"[*] Customer created: {username} / {password}")
    else:
        print(f"[!] User {username} already exists.")

if __name__ == "__main__":
    create_customer()
