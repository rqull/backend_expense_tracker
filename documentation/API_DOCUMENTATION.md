# Expense Tracker API Documentation

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [Introduction](#introduction)
- [API Base URL](#api-base-url)
- [Authentication](#authentication)
- [Common Parameters](#common-parameters)
- [Error Handling](#error-handling)
- [API Endpoints](#api-endpoints)
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
   git clone <repository-url>
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

## Introduction

The Expense Tracker API allows you to manage personal finances by tracking expenses, setting budgets, and monitoring spending patterns. This RESTful API is built with FastAPI and provides comprehensive endpoints for expense management.

## API Base URL

```
http://localhost:8000
```

API documentation can be accessed at:

```
http://localhost:8000/docs
```

## Authentication

The API currently does not implement authentication. User management functionality is included in the models but not exposed through endpoints. Future versions will include proper authentication.

## Common Parameters

The following parameters are common across multiple endpoints:

- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return (pagination)

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request succeeded
- `201 Created`: A new resource was created successfully
- `400 Bad Request`: The request was invalid or cannot be served
- `404 Not Found`: The requested resource does not exist
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON object with a `detail` field explaining the error:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## API Endpoints

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

## Data Models

### Category

- `id`: Integer - Unique identifier
- `name`: String - Category name (unique)
- `description`: String (optional) - Description of the category
- `created_at`: DateTime - When the category was created
- `updated_at`: DateTime - When the category was last updated

### Account

- `id`: Integer - Unique identifier
- `name`: String - Account name (unique)
- `initial_balance`: Decimal - Starting balance for the account
- `created_at`: DateTime - When the account was created
- `updated_at`: DateTime - When the account was last updated

### Tag

- `id`: Integer - Unique identifier
- `name`: String - Tag name (unique)
- `created_at`: DateTime - When the tag was created
- `updated_at`: DateTime - When the tag was last updated

### Expense

- `id`: Integer - Unique identifier
- `amount`: Decimal - Expense amount (positive value)
- `date`: Date - When the expense occurred
- `description`: String (optional) - Description of the expense
- `category_id`: Integer - Reference to the category
- `account_id`: Integer (optional) - Reference to the account
- `receipt_path`: String (optional) - Path to receipt image/file
- `created_at`: DateTime - When the expense was created
- `updated_at`: DateTime - When the expense was last updated
- `category`: Category - Related category object
- `account`: Account (optional) - Related account object
- `tags`: Array of Tag - Related tags

### Budget

- `id`: Integer - Unique identifier
- `category_id`: Integer - Reference to the category
- `year`: Integer - Budget year
- `month`: Integer - Budget month (1-12)
- `amount`: Decimal - Budget amount (positive value)
- `created_at`: DateTime - When the budget was created
- `updated_at`: DateTime - When the budget was last updated
- `category`: Category - Related category object

### RecurringExpense

- `id`: Integer - Unique identifier
- `name`: String - Name of the recurring expense
- `amount`: Decimal - Expense amount (positive value)
- `category_id`: Integer - Reference to the category
- `interval`: String - Frequency ("daily", "weekly", "biweekly", "monthly", "quarterly", "yearly")
- `next_date`: Date - Next occurrence date
- `end_date`: Date (optional) - When to stop generating expenses
- `created_at`: DateTime - When the recurring expense was created
- `updated_at`: DateTime - When the recurring expense was last updated
- `category`: Category - Related category object

### BudgetStatus

- `category_id`: Integer - Reference to the category
- `category_name`: String - Name of the category
- `budget_amount`: Decimal - Budgeted amount
- `total_spent`: Decimal - Actual spent amount
- `percent`: Float - Percentage of budget used

## Development Guide

### Code Organization

- **Routes**: Add new endpoints in `app/routers/`
- **Models**: Define database models in `app/models.py`
- **Schemas**: Define request/response schemas in `app/schemas.py`
- **CRUD**: Implement database operations in `app/crud.py`

### Best Practices

1. **Code Style**

   - Follow PEP 8
   - Use type hints
   - Document functions with docstrings

2. **Database**

   - Use SQLAlchemy ORM
   - Create migrations for schema changes
   - Test queries for performance

3. **API Design**
   - Use appropriate HTTP methods
   - Return proper status codes
   - Validate input data
   - Handle errors gracefully

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```
   ERROR: Could not connect to PostgreSQL
   ```
   **Solutions**:
   - Check if PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists
2. **Missing Dependencies**

   ```
   ImportError: No module named 'fastapi'
   ```

   **Solution**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Migration Errors**
   ```
   ERROR: Target database is not up to date
   ```
   **Solution**:
   ```bash
   python -m migrations.create_tables --force
   ```

### Getting Help

- Check the GitHub Issues
- Join our Discord community
- Email support: mm.rizqullah@gmail.com
