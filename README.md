# Inventory Management System - Backend

A Django REST Framework API for an inventory management with JWT authentication, SendGrid email and PostgreSQL Database


Live Url: https://inventory-management-7rem.onrender.com

Tech Stack:
- Python
- Django
- Django Rest Framework
- PostgreSQL Database
- JWT Authentication
- SendGrid
- Whitenoise
- Gunicorn

Features:
- User registration, login, and profile management
- JWT-based authentication with token refresh
- Password reset via SendGrid email
- Inventory item CRUD with category management
- Stock level validation (no negative stock)
- Low stock alerts via SendGrid email
- Audit history for stock changes
- Search, filter, and ordering on inventory items
- User data isolation (users only see their own data)

### Steps
```bash
git clone https://github.com/Harshi-code760/inventory-management-middleware
cd inventory-management-middleware/inventory-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Running Tests
```bash
python manage.py test
```

Tests cover:
- Negative stock prevention
- Audit history creation on stock change
- Category user isolation
- Low stock email alert triggered
- No alert sent when stock is above threshold
- Unauthenticated access blocked
- Profile update

## Architecture Decisions

- **Custom user model** — uses email as the primary login field instead of username, making it more enterprise-appropriate
- **JWT authentication** — stateless, scalable authentication suitable for a decoupled frontend/backend architecture
- **SendGrid** — external email service used for both low stock alerts and password reset, separating email infrastructure from application logic
- **User data isolation** — all querysets filter by the authenticated user, ensuring users can only access their own data
- **Audit history** — every stock change is recorded with old value, new value, user, and timestamp
- **Whitenoise** — serves static files efficiently without needing a separate CDN
