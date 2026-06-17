🍕 FastAPI Pizza Order Management API

A backend REST API developed with FastAPI for managing pizza orders, users, authentication, and authorization.

This project was created to practice backend development concepts such as API creation, database integration, user authentication with JWT, authorization levels, and object relationships using SQLAlchemy.

---

Technologies:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- OAuth2 Password Flow
- Passlib (Bcrypt)
- Pydantic
- Uvicorn
- Python Dotenv

---

Features:

Authentication & Users

- User account creation
- Password hashing using Bcrypt
- Login with JWT access token
- Refresh token generation
- Swagger Authorize button integration using OAuth2
- Protected endpoints with token validation

Orders:

- Create orders
- Add items to an order
- Remove items from an order
- Cancel orders
- Finalize orders
- View a specific order
- List all orders (admin only)
- List authenticated user orders

Authorization:

- Regular users can access and manage only their own orders
- Administrators can access and manage all orders

Database Relationships:

- One order can contain multiple items
- Automatic order price calculation based on items

---

Project Structure:

```text
fastapi-sqlalchemy-api/
│
├── auth_routes.py       # Authentication routes
├── order_routes.py      # Order management routes
├── models.py            # Database models
├── schemas.py           # Data validation schemas
├── dependencies.py      # Database sessions and JWT validation
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (not included in Git)
└── data.db              # SQLite database
```

---

Installation

1- Clone the repository

```bash
git clone https://github.com/BrendaCristiny/fastapi-sqlalchemy-api.git
```

2- Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

3- Install dependencies

```bash
pip install -r requirements.txt
```

---

4- Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

5- Run the API

```bash
uvicorn main:app --reload
```

The API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

Authentication Flow

1. Create an account using `/auth/create_account`
2. Login using `/auth/login-form`
3. Click the **Authorize** button in Swagger
4. Enter your credentials
5. Access protected endpoints using the generated token

---

This project allowed me to practice:

- REST API development
- API modularization
- Database modeling
- SQLAlchemy ORM
- Relationships between tables
- Authentication and authorization
- JWT tokens
- Dependency Injection with FastAPI
- Password encryption
- Environment variables management
- API documentation with Swagger

---

Future Improvements

Some improvements that can be implemented in the future:

- Database migrations using Alembic
- Docker containerization
- Automated tests with Pytest
- Better exception handling
- Pagination for large data queries
- Role-based permissions with more granular control

---

Developed by **Brenda Cristiny**.
