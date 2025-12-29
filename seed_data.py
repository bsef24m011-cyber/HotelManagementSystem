import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_project.settings")
django.setup()

from apps.rooms.models import Room, RoomType
from apps.food.models import FoodItem

def seed_data():
    print("[*] Seeding Database...")

    # 1. Room Types
    types = [
        ('Deluxe Suite', 250.00, 2, 'Luxury suite with city view'),
        ('Executive Room', 180.00, 2, 'Spacious room with work desk'),
        ('Standard Room', 100.00, 2, 'Cozy room for short stays'),
        ('Presidential Suite', 1000.00, 4, 'Top floor, panoramic view, jacuzzi'),
    ]
    
    room_type_objs = []
    for name, price, cap, desc in types:
        rt, created = RoomType.objects.get_or_create(
            name=name,
            defaults={'price_per_night': price, 'capacity': cap, 'description': desc}
        )
        room_type_objs.append(rt)
        if created:
            print(f"Created Room Type: {name}")
        else:
            print(f"Existing Room Type: {name}")

    # 2. Rooms
    # Create 5 rooms for each type
    for rt in room_type_objs:
        for i in range(1, 6):
            # Generate room number like 101, 102... or 201, 202... based on index
            room_num = f"{random.randint(100, 999)}"
            if not Room.objects.filter(number=room_num).exists():
                Room.objects.create(number=room_num, room_type=rt)
                print(f"Created Room {room_num} ({rt.name})")

    # 3. Food Items
    food_items = [
        ('Club Sandwich', 15.00, 'Club sandwich with turkey and bacon'),
        ('Caesar Salad', 12.50, 'Fresh romaine with parmesan'),
        ('Grilled Salmon', 28.00, 'Served with asparagus'),
        ('Cheeseburger', 18.00, 'Angus beef with cheddar'),
        ('Pasta Carbonara', 22.00, 'Creamy sauce with pancetta'),
        ('Tiramisu', 10.00, 'Italian coffee dessert'),
    ]

    for name, price, desc in food_items:
        f, created = FoodItem.objects.get_or_create(
            name=name,
            defaults={'price': price, 'description': desc}
        )
        if created:
            print(f"Created Food: {name}")

    print("[+] Database Seeded Successfully!")

if __name__ == "__main__":
    seed_data()
