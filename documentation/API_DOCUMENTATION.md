# Expense Tracker API Documentation

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [Authentication](#authentication)
- [API Base URL](#api-base-url)
- [Common Parameters](#common-parameters)
- [Error Handling](#error-handling)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication-endpoints)
  - [Health Check](#health-check)
  - [Categories](#categories)
  - [Expenses](#expenses)
  - [Budgets](#budgets)
  - [Accounts](#accounts)
  - [Tags](#tags)
  - [Recurring Expenses](#recurring-expenses)
- [Data Models](#data-models)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Step-by-Step Installation

1. **Clone or Download the Project**

   ```bash
   git clone https://github.com/rqull/backend_expense_tracker.git
   cd expanse_tracker/backend
   ```

2. **Set Up Python Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment (Windows)
   .\.venv\Scripts\activate

   # Activate virtual environment (Linux/Mac)
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**

   - Install PostgreSQL if not already installed
   - Create a new database:
     ```sql
     CREATE DATABASE expense_tracker;
     ```
   - Configure database connection in `.env`:
     ```
     DATABASE_URL=postgresql://postgres:12345@localhost:5432/expense_tracker
     ```

5. **Initialize Database**

   ```bash
   # Run migrations
   python -m migrations.create_tables

   # (Optional) Add sample data
   python -m scripts.seed_data
   ```

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables
├── app/
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py          # CRUD operations
│   ├── deps.py          # Dependencies
│   └── routers/         # API route handlers
├── migrations/           # Database migrations
├── scripts/             # Utility scripts
└── documentation/       # API documentation
```

## Running the Project

1. **Start the Server**

   ```bash
   # Development mode with auto-reload
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Production mode
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Access the API**

   - Main API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Verify Installation**
   ```bash
   # Check API health
   curl http://localhost:8000/health
   ```

## Authentication

The API uses JWT (JSON Web Token) for authentication. To access protected endpoints, you need to:

1. Register a new user account
2. Login to get an access token
3. Include the token in the Authorization header of subsequent requests

### Authentication Flow

1. **Register**: Create a new user account
   - Endpoint: POST /auth/register
   - No authentication required
2. **Login**: Get access token
   - Endpoint: POST /auth/token
   - Use credentials to get JWT token
3. **Access Protected Resources**:
   - Include token in Authorization header
   - Format: `Authorization: Bearer <your-token>`

### Token Format

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- Access tokens expire after 30 minutes
- You need to login again to get a new token

## API Endpoints

### Authentication Endpoints

#### POST /auth/register

Register a new user account.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "strongpassword123"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2025-06-13T10:00:00"
}
```

#### POST /auth/token

Login to get access token.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "strongpassword123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /auth/me

Get current user information.

**Headers:**

```
Authorization: Bearer <your-token>
```

**Response:**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2025-06-13T10:00:00"
}
```

### Protected Endpoints

All endpoints below require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

### Health Check

#### GET /health

Checks if the API is running.

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-06-12T10:00:00.123456"
}
```

### Categories

Categories help organize expenses into meaningful groups.

#### GET /categories/

Retrieve all expense categories.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Transportation",
    "description": "Public transport and fuel",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

#### GET /categories/{id}

Retrieve a specific category by ID.

**Path Parameters:**

- `id`: The unique identifier of the category

**Response:**

```json
{
  "id": 1,
  "name": "Food",
  "description": "Groceries and eating out",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

#### POST /categories/

Create a new expense category.

**Request Body:**

```json
{
  "name": "Entertainment",
  "description": "Movies, games, and other entertainment expenses"
}
```

**Response:**

```json
{
  "id": 3,
  "name": "Entertainment",
  "description": "Movies, games, and other entertainment expenses",
  "created_at": "2025-06-12T10:30:00",
  "updated_at": "2025-06-12T10:30:00"
}
```

#### PUT /categories/{id}

Update an existing category.

**Path Parameters:**

- `id`: The unique identifier of the category

**Request Body:**

```json
{
  "name": "Entertainment & Leisure",
  "description": "Updated description"
}
```

**Response:**

```json
{
  "id": 3,
  "name": "Entertainment & Leisure",
  "description": "Updated description",
  "created_at": "2025-06-12T10:30:00",
  "updated_at": "2025-06-12T10:45:00"
}
```

#### DELETE /categories/{id}

Delete a category.

**Path Parameters:**

- `id`: The unique identifier of the category

**Response:**

```json
{
  "message": "Category deleted successfully"
}
```

### Expenses

Expenses represent individual financial transactions.

#### GET /expenses/

Retrieve all expenses with optional filtering.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)
- `category_id` (optional): Filter expenses by category ID
- `account_id` (optional): Filter expenses by account ID
- `start_date` (optional): Filter expenses with date >= start_date (format: YYYY-MM-DD)
- `end_date` (optional): Filter expenses with date <= end_date (format: YYYY-MM-DD)

**Response:**

```json
[
  {
    "id": 1,
    "amount": "35.50",
    "date": "2025-06-10",
    "description": "Grocery shopping",
    "category_id": 1,
    "account_id": 2,
    "receipt_path": null,
    "created_at": "2025-06-10T15:30:00",
    "updated_at": "2025-06-10T15:30:00",
    "category": {
      "id": 1,
      "name": "Food",
      "description": "Groceries and eating out"
    },
    "account": {
      "id": 2,
      "name": "Bank Account",
      "initial_balance": "2500.00"
    },
    "tags": [
      {
        "id": 1,
        "name": "Essential"
      }
    ]
  }
]
```

#### GET /expenses/{id}

Retrieve a specific expense by ID.

**Path Parameters:**

- `id`: The unique identifier of the expense

**Response:**

```json
{
  "id": 1,
  "amount": "35.50",
  "date": "2025-06-10",
  "description": "Grocery shopping",
  "category_id": 1,
  "account_id": 2,
  "receipt_path": null,
  "created_at": "2025-06-10T15:30:00",
  "updated_at": "2025-06-10T15:30:00",
  "category": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out"
  },
  "account": {
    "id": 2,
    "name": "Bank Account",
    "initial_balance": "2500.00"
  },
  "tags": [
    {
      "id": 1,
      "name": "Essential"
    }
  ]
}
```

#### POST /expenses/

Create a new expense.

**Request Body:**

```json
{
  "amount": 42.99,
  "date": "2025-06-12",
  "description": "Dinner at restaurant",
  "category_id": 1,
  "account_id": 2,
  "tag_ids": [1, 4],
  "receipt_path": null
}
```

**Response:**

```json
{
  "id": 5,
  "amount": "42.99",
  "date": "2025-06-12",
  "description": "Dinner at restaurant",
  "category_id": 1,
  "account_id": 2,
  "receipt_path": null,
  "created_at": "2025-06-12T11:15:00",
  "updated_at": "2025-06-12T11:15:00",
  "category": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out"
  },
  "account": {
    "id": 2,
    "name": "Bank Account",
    "initial_balance": "2500.00"
  },
  "tags": [
    {
      "id": 1,
      "name": "Essential"
    },
    {
      "id": 4,
      "name": "Personal"
    }
  ]
}
```

#### PUT /expenses/{id}

Update an existing expense.

**Path Parameters:**

- `id`: The unique identifier of the expense

**Request Body:**

```json
{
  "amount": 45.99,
  "description": "Updated dinner description",
  "tag_ids": [1, 2, 4]
}
```

**Response:**

```json
{
  "id": 5,
  "amount": "45.99",
  "date": "2025-06-12",
  "description": "Updated dinner description",
  "category_id": 1,
  "account_id": 2,
  "receipt_path": null,
  "created_at": "2025-06-12T11:15:00",
  "updated_at": "2025-06-12T11:30:00",
  "category": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out"
  },
  "account": {
    "id": 2,
    "name": "Bank Account",
    "initial_balance": "2500.00"
  },
  "tags": [
    {
      "id": 1,
      "name": "Essential"
    },
    {
      "id": 2,
      "name": "Luxury"
    },
    {
      "id": 4,
      "name": "Personal"
    }
  ]
}
```

#### DELETE /expenses/{id}

Delete an expense.

**Path Parameters:**

- `id`: The unique identifier of the expense

**Response:**

```json
{
  "message": "Expense deleted successfully"
}
```

### Budgets

Budgets set spending limits for categories within a specific month.

#### GET /budgets/

Retrieve all budgets.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "category_id": 1,
    "year": 2025,
    "month": 6,
    "amount": "300.00",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00",
    "category": {
      "id": 1,
      "name": "Food",
      "description": "Groceries and eating out"
    }
  }
]
```

#### GET /budgets/{id}

Retrieve a specific budget by ID.

**Path Parameters:**

- `id`: The unique identifier of the budget

**Response:**

```json
{
  "id": 1,
  "category_id": 1,
  "year": 2025,
  "month": 6,
  "amount": "300.00",
  "created_at": "2025-06-01T00:00:00",
  "updated_at": "2025-06-01T00:00:00",
  "category": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out"
  }
}
```

#### POST /budgets/

Create a new budget.

**Request Body:**

```json
{
  "category_id": 2,
  "year": 2025,
  "month": 6,
  "amount": 150.0
}
```

**Response:**

```json
{
  "id": 2,
  "category_id": 2,
  "year": 2025,
  "month": 6,
  "amount": "150.00",
  "created_at": "2025-06-12T12:00:00",
  "updated_at": "2025-06-12T12:00:00",
  "category": {
    "id": 2,
    "name": "Transportation",
    "description": "Public transport and fuel"
  }
}
```

#### PUT /budgets/{id}

Update an existing budget.

**Path Parameters:**

- `id`: The unique identifier of the budget

**Request Body:**

```json
{
  "amount": 200.0
}
```

**Response:**

```json
{
  "id": 2,
  "category_id": 2,
  "year": 2025,
  "month": 6,
  "amount": "200.00",
  "created_at": "2025-06-12T12:00:00",
  "updated_at": "2025-06-12T12:15:00",
  "category": {
    "id": 2,
    "name": "Transportation",
    "description": "Public transport and fuel"
  }
}
```

#### DELETE /budgets/{id}

Delete a budget.

**Path Parameters:**

- `id`: The unique identifier of the budget

**Response:**

```json
{
  "message": "Budget deleted successfully"
}
```

#### GET /budgets/status/

Get budget status for a specific month, showing planned vs. actual spending.

**Query Parameters:**

- `year` (required): Year for budget status
- `month` (required): Month for budget status (1-12)

**Response:**

```json
[
  {
    "category_id": 1,
    "category_name": "Food",
    "budget_amount": "300.00",
    "total_spent": "78.49",
    "percent": 26.16
  },
  {
    "category_id": 2,
    "category_name": "Transportation",
    "budget_amount": "200.00",
    "total_spent": "12.00",
    "percent": 6.0
  }
]
```

### Accounts

Accounts represent different sources of funds like cash, bank accounts, or credit cards.

#### GET /accounts/

Retrieve all accounts.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Cash",
    "initial_balance": "500.00",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Bank Account",
    "initial_balance": "2500.00",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  }
]
```

#### GET /accounts/{id}

Retrieve a specific account by ID.

**Path Parameters:**

- `id`: The unique identifier of the account

**Response:**

```json
{
  "id": 1,
  "name": "Cash",
  "initial_balance": "500.00",
  "created_at": "2025-06-01T00:00:00",
  "updated_at": "2025-06-01T00:00:00"
}
```

#### POST /accounts/

Create a new account.

**Request Body:**

```json
{
  "name": "Savings Account",
  "initial_balance": 5000.0
}
```

**Response:**

```json
{
  "id": 4,
  "name": "Savings Account",
  "initial_balance": "5000.00",
  "created_at": "2025-06-12T13:00:00",
  "updated_at": "2025-06-12T13:00:00"
}
```

#### PUT /accounts/{id}

Update an existing account.

**Path Parameters:**

- `id`: The unique identifier of the account

**Request Body:**

```json
{
  "name": "Savings Account (High Interest)",
  "initial_balance": 5500.0
}
```

**Response:**

```json
{
  "id": 4,
  "name": "Savings Account (High Interest)",
  "initial_balance": "5500.00",
  "created_at": "2025-06-12T13:00:00",
  "updated_at": "2025-06-12T13:15:00"
}
```

#### DELETE /accounts/{id}

Delete an account.

**Path Parameters:**

- `id`: The unique identifier of the account

**Response:**

```json
{
  "message": "Account deleted successfully"
}
```

### Tags

Tags are labels that can be applied to expenses for more detailed categorization.

#### GET /tags/

Retrieve all tags.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Essential",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Luxury",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  }
]
```

#### GET /tags/{id}

Retrieve a specific tag by ID.

**Path Parameters:**

- `id`: The unique identifier of the tag

**Response:**

```json
{
  "id": 1,
  "name": "Essential",
  "created_at": "2025-06-01T00:00:00",
  "updated_at": "2025-06-01T00:00:00"
}
```

#### POST /tags/

Create a new tag.

**Request Body:**

```json
{
  "name": "Travel"
}
```

**Response:**

```json
{
  "id": 5,
  "name": "Travel",
  "created_at": "2025-06-12T14:00:00",
  "updated_at": "2025-06-12T14:00:00"
}
```

#### PUT /tags/{id}

Update an existing tag.

**Path Parameters:**

- `id`: The unique identifier of the tag

**Request Body:**

```json
{
  "name": "Travel & Vacation"
}
```

**Response:**

```json
{
  "id": 5,
  "name": "Travel & Vacation",
  "created_at": "2025-06-12T14:00:00",
  "updated_at": "2025-06-12T14:15:00"
}
```

#### DELETE /tags/{id}

Delete a tag.

**Path Parameters:**

- `id`: The unique identifier of the tag

**Response:**

```json
{
  "message": "Tag deleted successfully"
}
```

### Recurring Expenses

Recurring expenses are regularly occurring expenses that are automatically generated.

#### GET /recurring/

Retrieve all recurring expenses.

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Monthly Rent",
    "amount": "800.00",
    "category_id": 3,
    "interval": "monthly",
    "next_date": "2025-07-01",
    "end_date": null,
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00",
    "category": {
      "id": 3,
      "name": "Housing",
      "description": "Rent, mortgage, and utilities"
    }
  }
]
```

#### GET /recurring/{id}

Retrieve a specific recurring expense by ID.

**Path Parameters:**

- `id`: The unique identifier of the recurring expense

**Response:**

```json
{
  "id": 1,
  "name": "Monthly Rent",
  "amount": "800.00",
  "category_id": 3,
  "interval": "monthly",
  "next_date": "2025-07-01",
  "end_date": null,
  "created_at": "2025-06-01T00:00:00",
  "updated_at": "2025-06-01T00:00:00",
  "category": {
    "id": 3,
    "name": "Housing",
    "description": "Rent, mortgage, and utilities"
  }
}
```

#### POST /recurring/

Create a new recurring expense.

**Request Body:**

```json
{
  "name": "Internet Subscription",
  "amount": 59.99,
  "category_id": 3,
  "interval": "monthly",
  "next_date": "2025-07-15",
  "end_date": null
}
```

**Response:**

```json
{
  "id": 4,
  "name": "Internet Subscription",
  "amount": "59.99",
  "category_id": 3,
  "interval": "monthly",
  "next_date": "2025-07-15",
  "end_date": null,
  "created_at": "2025-06-12T15:00:00",
  "updated_at": "2025-06-12T15:00:00",
  "category": {
    "id": 3,
    "name": "Housing",
    "description": "Rent, mortgage, and utilities"
  }
}
```

#### PUT /recurring/{id}

Update an existing recurring expense.

**Path Parameters:**

- `id`: The unique identifier of the recurring expense

**Request Body:**

```json
{
  "amount": 64.99,
  "interval": "monthly",
  "next_date": "2025-07-20"
}
```

**Response:**

```json
{
  "id": 4,
  "name": "Internet Subscription",
  "amount": "64.99",
  "category_id": 3,
  "interval": "monthly",
  "next_date": "2025-07-20",
  "end_date": null,
  "created_at": "2025-06-12T15:00:00",
  "updated_at": "2025-06-12T15:15:00",
  "category": {
    "id": 3,
    "name": "Housing",
    "description": "Rent, mortgage, and utilities"
  }
}
```

#### DELETE /recurring/{id}

Delete a recurring expense.

**Path Parameters:**

- `id`: The unique identifier of the recurring expense

**Response:**

```json
{
  "message": "Recurring expense deleted successfully"
}
```

#### POST /recurring/generate/

Generate expenses from due recurring expenses.

**Response:**

```json
[
  {
    "id": 10,
    "amount": "800.00",
    "date": "2025-06-01",
    "description": "Auto-generated from recurring: Monthly Rent",
    "category_id": 3,
    "account_id": null,
    "receipt_path": null,
    "created_at": "2025-06-12T15:30:00",
    "updated_at": "2025-06-12T15:30:00",
    "category": {
      "id": 3,
      "name": "Housing",
      "description": "Rent, mortgage, and utilities"
    },
    "account": null,
    "tags": []
  }
]
```

## Error Handling

### Authentication Errors

- **401 Unauthorized**: Invalid or expired token

  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```

- **401 Unauthorized**: Invalid login credentials

  ```json
  {
    "detail": "Incorrect username or password"
  }
  ```

- **400 Bad Request**: Registration validation error
  ```json
  {
    "detail": "Username already registered"
  }
  ```

### Common Errors

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Each error response includes a detail message:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Security Best Practices

1. **Password Security**

   - Passwords must be at least 8 characters
   - Should include numbers and special characters
   - Never send passwords in plain text

2. **Token Security**

   - Store tokens securely
   - Never share tokens
   - Tokens expire after 30 minutes

3. **API Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Regular security audits

## Development Guide

### Authentication Implementation

1. **Setup Environment**

   ```bash
   # Add to .env file
   SECRET_KEY="your-secret-key-here"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. **Making Authenticated Requests**

   ```python
   import requests

   # Login
   response = requests.post(
       "http://localhost:8000/auth/token",
       data={"username": "johndoe", "password": "password123"}
   )
   token = response.json()["access_token"]

   # Use token in subsequent requests
   headers = {"Authorization": f"Bearer {token}"}
   response = requests.get(
       "http://localhost:8000/expenses",
       headers=headers
   )
   ```

[... rest of the existing documentation ...]
