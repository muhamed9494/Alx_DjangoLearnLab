# Social Media API - User Authentication

## Features
- User Registration with token generation
- User Login with token retrieval

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Run the server: `python manage.py runserver`

## Endpoints
- `POST /api/accounts/register/` - Register a new user.
- `POST /api/accounts/login/` - Login and retrieve an authentication token.
