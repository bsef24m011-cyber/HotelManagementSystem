import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_project.settings")
django.setup()

from apps.users.models import User

def ensure_admin():
    username = "admin"
    password = "admin"
    email = "admin@hotel.com"
    
    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'ADMIN'
        user.save()
        print(f"[*] Password for '{username}' reset to '{password}'.")
    else:
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
            role='ADMIN'
        )
        print(f"[*] Admin user '{username}' created with password '{password}'.")

if __name__ == "__main__":
    ensure_admin()
