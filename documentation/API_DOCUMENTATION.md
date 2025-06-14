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

## API Response Format

All API endpoints follow a consistent response format:

```json
{
  "status": "success" | "error",
  "data": <response_data>,
  "message": "Optional message describing the result"
}
```

### Success Response Example

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out"
  },
  "message": "Category created successfully"
}
```

### Error Response Example

```json
{
  "status": "error",
  "data": null,
  "message": "Category with ID 123 not found"
}
```

### List Response Example

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Food",
        "description": "Groceries and eating out"
      },
      {
        "id": 2,
        "name": "Transportation",
        "description": "Public transport and fuel"
      }
    ],
    "total": 2,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

### Pagination

For endpoints that return lists, the following query parameters are supported:

- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 10)
- `sort` (optional): Sort field (default varies by endpoint)
- `order` (optional): Sort order, "asc" or "desc" (default: "asc")

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
  "status": "success",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2025-06-13T10:00:00"
  },
  "message": "User registered successfully"
}
```

**Error Response:**

```json
{
  "status": "error",
  "data": null,
  "message": "Username already registered"
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
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "message": "Successfully logged in"
}
```

**Error Response:**

```json
{
  "status": "error",
  "data": null,
  "message": "Invalid username or password"
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
  "status": "success",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2025-06-13T10:00:00"
  },
  "message": null
}
```

**Error Response:**

```json
{
  "status": "error",
  "data": null,
  "message": "Invalid or expired token"
}
```

### Categories

#### GET /categories/

Retrieve all expense categories.

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 10)
- `sort` (optional): Sort field (default: "name")
- `order` (optional): Sort order, "asc" or "desc" (default: "asc")

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
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
    ],
    "total": 2,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /categories/{id}

Retrieve a specific category by ID.

**Path Parameters:**

- `id`: The unique identifier of the category

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Food",
    "description": "Groceries and eating out",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  "message": null
}
```

**Error Response:**

```json
{
  "status": "error",
  "data": null,
  "message": "Category not found"
}
```

### Expenses

Expenses represent individual financial transactions.

#### GET /expenses/

Retrieve all expenses with optional filtering.

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 10)
- `sort` (optional): Sort field (default: "date")
- `order` (optional): Sort order, "asc" or "desc" (default: "desc")
- `category_id` (optional): Filter expenses by category ID
- `account_id` (optional): Filter expenses by account ID
- `start_date` (optional): Filter expenses with date >= start_date (format: YYYY-MM-DD)
- `end_date` (optional): Filter expenses with date <= end_date (format: YYYY-MM-DD)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "amount": "35.50",
        "date": "2025-06-10",
        "description": "Grocery shopping",
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
        ],
        "receipt_path": null,
        "created_at": "2025-06-10T15:30:00",
        "updated_at": "2025-06-10T15:30:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /expenses/{id}

Retrieve a specific expense by ID.

**Path Parameters:**

- `id`: The unique identifier of the expense

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "amount": "35.50",
    "date": "2025-06-10",
    "description": "Grocery shopping",
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
    ],
    "receipt_path": null,
    "created_at": "2025-06-10T15:30:00",
    "updated_at": "2025-06-10T15:30:00"
  },
  "message": null
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
  "status": "success",
  "data": {
    "id": 5,
    "amount": "42.99",
    "date": "2025-06-12",
    "description": "Dinner at restaurant",
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
    ],
    "receipt_path": null,
    "created_at": "2025-06-12T11:15:00",
    "updated_at": "2025-06-12T11:15:00"
  },
  "message": "Expense created successfully"
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
  "status": "success",
  "data": {
    "id": 5,
    "amount": "45.99",
    "date": "2025-06-12",
    "description": "Updated dinner description",
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
    ],
    "receipt_path": null,
    "created_at": "2025-06-12T11:15:00",
    "updated_at": "2025-06-12T11:30:00"
  },
  "message": "Expense updated successfully"
}
```

#### DELETE /expenses/{id}

Delete an expense.

**Path Parameters:**

- `id`: The unique identifier of the expense

**Response:**

```json
{
  "status": "success",
  "data": null,
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
{
  "status": "success",
  "data": {
    "items": [
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
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /budgets/{id}

Retrieve a specific budget by ID.

**Path Parameters:**

- `id`: The unique identifier of the budget

**Response:**

```json
{
  "status": "success",
  "data": {
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
  },
  "message": null
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
  "status": "success",
  "data": {
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
  },
  "message": "Budget created successfully"
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
  "status": "success",
  "data": {
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
  },
  "message": "Budget updated successfully"
}
```

#### DELETE /budgets/{id}

Delete a budget.

**Path Parameters:**

- `id`: The unique identifier of the budget

**Response:**

```json
{
  "status": "success",
  "data": null,
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
{
  "status": "success",
  "data": {
    "summary": {
      "total_budget": "500.00",
      "total_spent": "90.49",
      "percent": 18.1
    },
    "categories": [
      {
        "category_id": 1,
        "category_name": "Food",
        "budget_amount": "300.00",
        "total_spent": "78.49",
        "percent": 26.16,
        "status": "on_track"
      },
      {
        "category_id": 2,
        "category_name": "Transportation",
        "budget_amount": "200.00",
        "total_spent": "12.00",
        "percent": 6.0,
        "status": "on_track"
      }
    ]
  },
  "message": null
}
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
{
  "status": "success",
  "data": {
    "items": [
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
    ],
    "total": 2,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /accounts/{id}

Retrieve a specific account by ID.

**Path Parameters:**

- `id`: The unique identifier of the account

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Cash",
    "initial_balance": "500.00",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  },
  "message": null
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
  "status": "success",
  "data": {
    "id": 4,
    "name": "Savings Account",
    "initial_balance": "5000.00",
    "created_at": "2025-06-12T13:00:00",
    "updated_at": "2025-06-12T13:00:00"
  },
  "message": "Account created successfully"
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
  "status": "success",
  "data": {
    "id": 4,
    "name": "Savings Account (High Interest)",
    "initial_balance": "5500.00",
    "created_at": "2025-06-12T13:00:00",
    "updated_at": "2025-06-12T13:15:00"
  },
  "message": "Account updated successfully"
}
```

#### DELETE /accounts/{id}

Delete an account.

**Path Parameters:**

- `id`: The unique identifier of the account

**Response:**

```json
{
  "status": "success",
  "data": null,
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
{
  "status": "success",
  "data": {
    "items": [
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
    ],
    "total": 2,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /tags/{id}

Retrieve a specific tag by ID.

**Path Parameters:**

- `id`: The unique identifier of the tag

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Essential",
    "created_at": "2025-06-01T00:00:00",
    "updated_at": "2025-06-01T00:00:00"
  },
  "message": null
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
  "status": "success",
  "data": {
    "id": 5,
    "name": "Travel",
    "created_at": "2025-06-12T14:00:00",
    "updated_at": "2025-06-12T14:00:00"
  },
  "message": "Tag created successfully"
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
  "status": "success",
  "data": {
    "id": 5,
    "name": "Travel & Vacation",
    "created_at": "2025-06-12T14:00:00",
    "updated_at": "2025-06-12T14:15:00"
  },
  "message": "Tag updated successfully"
}
```

#### DELETE /tags/{id}

Delete a tag.

**Path Parameters:**

- `id`: The unique identifier of the tag

**Response:**

```json
{
  "status": "success",
  "data": null,
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
{
  "status": "success",
  "data": {
    "items": [
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
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### GET /recurring/{id}

Retrieve a specific recurring expense by ID.

**Path Parameters:**

- `id`: The unique identifier of the recurring expense

**Response:**

```json
{
  "status": "success",
  "data": {
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
  },
  "message": null
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
  "status": "success",
  "data": {
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
  },
  "message": "Recurring expense created successfully"
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
  "status": "success",
  "data": {
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
  },
  "message": "Recurring expense updated successfully"
}
```

#### DELETE /recurring/{id}

Delete a recurring expense.

**Path Parameters:**

- `id`: The unique identifier of the recurring expense

**Response:**

```json
{
  "status": "success",
  "data": null,
  "message": "Recurring expense deleted successfully"
}
```

#### POST /recurring/generate/

Generate expenses from due recurring expenses.

**Response:**

```json
{
  "status": "success",
  "data": {
    "generated": [
      {
        "id": 10,
        "amount": "800.00",
        "date": "2025-06-01",
        "description": "Auto-generated from recurring: Monthly Rent",
        "category": {
          "id": 3,
          "name": "Housing",
          "description": "Rent, mortgage, and utilities"
        },
        "account": null,
        "tags": [],
        "receipt_path": null,
        "created_at": "2025-06-12T15:30:00",
        "updated_at": "2025-06-12T15:30:00"
      }
    ],
    "total_generated": 1,
    "next_generation_date": "2025-07-01"
  },
  "message": "Successfully generated recurring expenses"
}
```

## Error Handling

All error responses follow the standard format:

```json
{
  "status": "error",
  "data": null,
  "message": "Detailed error message"
}
```

### Common HTTP Status Codes

- **400 Bad Request**: Invalid input data or validation error
- **401 Unauthorized**: Authentication failed or invalid token
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate unique field)
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Error Examples

**Authentication Error (401):**

```json
{
  "status": "error",
  "data": null,
  "message": "Invalid or expired token"
}
```

**Validation Error (422):**

```json
{
  "status": "error",
  "data": {
    "errors": [
      {
        "field": "amount",
        "message": "Amount must be greater than 0"
      },
      {
        "field": "date",
        "message": "Date cannot be in the future"
      }
    ]
  },
  "message": "Validation failed"
}
```

**Rate Limit Error (429):**

```json
{
  "status": "error",
  "data": {
    "retry_after": 60
  },
  "message": "Rate limit exceeded. Please try again in 60 seconds."
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- Authentication endpoints: 5 requests per minute
- Other endpoints: 60 requests per minute per authenticated user

Rate limit response headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1623567890
```

When rate limit is exceeded:

- Status code: 429 Too Many Requests
- Response includes retry_after value in seconds
