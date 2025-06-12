# Expense Tracker API

A RESTful API built with FastAPI for tracking personal expenses, managing budgets, and monitoring spending patterns.

## Features

- ✅ Expense Management
- 📊 Budget Tracking
- 💰 Account Management
- 🏷️ Category and Tag Organization
- 🔄 Recurring Expenses
- 📈 Spending Analytics

## Tech Stack

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Quick Start

1. **Clone the repository**

   ```powershell
   git clone <repository-url>
   cd expanse_tracker/backend
   ```

2. **Set up virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure database**

   - Create a PostgreSQL database
   - Copy `.env.example` to `.env` and update the database connection string

   ```
   DATABASE_URL=postgresql://postgres:12345@localhost:5432/expense_tracker
   ```

5. **Initialize database**

   ```powershell
   python -m migrations.create_tables
   python -m scripts.seed_data  # Optional: Add sample data
   ```

6. **Run the application**

   ```powershell
   uvicorn main:app --reload
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

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

## API Documentation

For detailed API documentation, please refer to [API_DOCUMENTATION.md](documentation/API_DOCUMENTATION.md).

## Development

1. **Create a new branch**

   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. **Run tests**

   ```powershell
   pytest
   ```

3. **Check code style**
   ```powershell
   flake8
   black .
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
