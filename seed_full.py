import os
import django
import random
from datetime import date, timedelta, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_project.settings")
django.setup()

from apps.users.models import User
from apps.rooms.models import Room, RoomType
from apps.bookings.models import Booking
from apps.food.models import FoodItem, FoodOrder, OrderItem
from apps.events.models import Event
from apps.billing.models import Invoice, Payment
from apps.payroll.models import StaffSalary, PayrollRecord

def seed_everything():
    print("[*] Starting Comprehensive Seeding...")

    # 1. Users
    print("    - Seeding Users...")
    customers = []
    for i in range(1, 4):
        u, c = User.objects.get_or_create(username=f"customer{i}", defaults={
            "email": f"customer{i}@example.com",
            "role": "CUSTOMER"
        })
        if c: u.set_password("password123"); u.save()
        customers.append(u)
    
    staff_members = []
    for i in range(1, 3):
        u, c = User.objects.get_or_create(username=f"staff{i}", defaults={
            "email": f"staff{i}@hotel.com",
            "role": "STAFF"
        })
        if c: u.set_password("password123"); u.save()
        staff_members.append(u)

    # 2. Rooms (already done by previous script but ensuring consistency)
    print("    - Seeding Room Types...")
    types_data = [
        ('Deluxe Suite', 250.00, 2),
        ('Executive Room', 180.00, 2),
        ('Standard Room', 100.00, 2),
        ('Presidential Suite', 1000.00, 4),
    ]
    room_types = []
    for name, price, cap in types_data:
        rt, _ = RoomType.objects.get_or_create(name=name, defaults={"price_per_night": price, "capacity": cap})
        room_types.append(rt)

    print("    - Seeding Rooms...")
    rooms = []
    for rt in room_types:
        for i in range(1, 4):
            num = f"{room_types.index(rt)+1}0{i}"
            r, _ = Room.objects.get_or_create(number=num, defaults={"room_type": rt})
            rooms.append(r)

    # 3. Bookings
    print("    - Seeding Bookings...")
    sample_bookings = []
    today = date.today()
    for i, customer in enumerate(customers):
        # Current Booking
        b1 = Booking.objects.create(
            user=customer,
            room=rooms[i % len(rooms)],
            check_in_date=today,
            check_out_date=today + timedelta(days=3),
            status="CONFIRMED"
        )
        sample_bookings.append(b1)
        # Past Booking
        b2 = Booking.objects.create(
            user=customer,
            room=rooms[(i+5) % len(rooms)],
            check_in_date=today - timedelta(days=10),
            check_out_date=today - timedelta(days=7),
            status="COMPLETED"
        )
        sample_bookings.append(b2)

    # 4. Food
    print("    - Seeding Food Items...")
    foods = [
        ('Club Sandwich', 15.00),
        ('Caesar Salad', 12.00),
        ('Steak', 35.00),
        ('Pasta', 20.00)
    ]
    food_objs = []
    for name, price in foods:
        f, _ = FoodItem.objects.get_or_create(name=name, defaults={"price": price})
        food_objs.append(f)

    print("    - Seeding Food Orders...")
    for b in sample_bookings[:3]: # Add orders to first 3 bookings
        order = FoodOrder.objects.create(booking=b, status="DELIVERED")
        OrderItem.objects.create(order=order, food_item=random.choice(food_objs), quantity=2)

    # 5. Events
    print("    - Seeding Events...")
    Event.objects.create(
        client=customers[0],
        event_type="WEDDING",
        date=today + timedelta(days=30),
        start_time=time(18, 0),
        end_time=time(23, 0),
        attendees=100,
        price=5000.00,
        status="CONFIRMED"
    )

    # 6. Billing
    print("    - Seeding Invoices & Payments...")
    for b in sample_bookings:
        inv = Invoice.objects.create(
            user=b.user,
            booking=b,
            amount=500.00,
            status="PAID" if b.status == "COMPLETED" else "UNPAID"
        )
        if inv.status == "PAID":
            Payment.objects.create(invoice=inv, amount=500.00, payment_method="CREDIT_CARD")

    # 7. Payroll
    print("    - Seeding Salaries & Payroll...")
    for s in staff_members:
        salary, _ = StaffSalary.objects.get_or_create(staff=s, defaults={"base_salary": 3000.00, "bonus": 200.00})
        PayrollRecord.objects.create(staff=s, amount_paid=3200.00, description="December 2025 Salary")

    print("[+] Seeding Complete! System is fully populated.")

if __name__ == "__main__":
    seed_everything()
