# Hotel Management System Backend

## Overview
A complete, production-ready backend for a Hotel Management System using Django and Django REST Framework.
Features module-based architecture, JWT authentication, and comprehensive management for users, rooms, bookings, food, events, billing, and payroll.

## Requirements
- Python 3.8+
- MySQL (or SQLite for dev)

## Setup Instructions
1. **Clone the repository** (if applicable)
2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt mysqlclient
   ```
3. **Database Setup**:
   - Ensure MySQL is running and create a database named `hms_db`.
   - Update `hms_project/settings.py` `DATABASES` configuration if needed.
4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Modules & Endpoints
- **Users**: `/api/users/` (Register, Login, Profile)
- **Rooms**: `/api/rooms/` (CRUD Rooms, Room Types)
- **Bookings**: `/api/bookings/` (Book rooms, check availability)
- **Food**: `/api/food/` (Menu, Orders)
- **Events**: `/api/events/` (Event booking)
- **Billing**: `/api/billing/` (Invoices, Payments, Revenue)
- **Payroll**: `/api/payroll/` (Staff Salaries)

## Authentication
Use the `/api/users/login/` endpoint to obtain a JWT pair (access/refresh).
Include the access token in the `Authorization` header: `Bearer <token>` for protected endpoints.
