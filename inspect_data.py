import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_project.settings")
django.setup()

from django.apps import apps
from django.contrib.auth import get_user_model

def inspect():
    print("--- Database Contents ---")
    
    # Users
    User = get_user_model()
    print(f"\nUsers ({User.objects.count()}):")
    for u in User.objects.all():
        print(f" - {u.username} (Role: {u.role})")

    # Inspect other app models
    app_labels = ['rooms', 'bookings', 'food', 'events', 'billing', 'payroll']
    
    for app_label in app_labels:
        print(f"\n[{app_label.upper()}]")
        app_config = apps.get_app_config(app_label)
        for model in app_config.get_models():
            count = model.objects.count()
            print(f" - {model.__name__}: {count}")
            if count > 0:
                # Print first 3 items
                for obj in model.objects.all()[:3]:
                    print(f"   * {obj}")

if __name__ == "__main__":
    inspect()
