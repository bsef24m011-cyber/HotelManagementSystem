# Luxuria Hotel Management System

A premium Hotel Management System built with Django and Vanilla JavaScript.

## Features
- **User Roles**: Admin, Staff, and Customer panels.
- **Room Management**: Dynamic booking and inventory.
- **Dining**: Integrated food ordering system.
- **Billing**: Automated invoice generation and payment tracking.
- **Security**: JWT Authentication and production-ready settings.

## Repository Structure
- `main`: The stable, production-ready code combining backend and frontend.
- `backend`: Focuses on the Django REST API, Models, and business logic.
- `frontend`: Focuses on Django Templates, Static CSS/JS, and UI components.

## Local Setup
1. Clone the repository.
2. Install dependencies: `pip install django djangorestframework djangorestframework-simplejwt django-cors-headers python-dotenv waitress whitenoise`.
3. Create a `.env` file (see `.env.example`).
4. Run migrations: `python manage.py migrate`.
5. Start server: `python run_prod.py`.

## Pushing to GitHub
To push this project to your GitHub:
1. Create a new repository on GitHub.
2. Run the following commands:
   ```bash
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   git push origin backend
   git push origin frontend
   ```
