# scripts/seed_data.py
import sys
import os
from datetime import date, timedelta
from decimal import Decimal

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, Account, Tag, Expense, Budget, RecurringExpense

def seed_database():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Category).count() > 0:
            print("Data already exists in the database. Skipping seeding.")
            return

        print("Seeding database with initial data...")

        # Create categories
        categories = [
            Category(name="Food", description="Groceries and eating out"),
            Category(name="Transportation", description="Public transport and fuel"),
            Category(name="Entertainment", description="Movies, games, and fun activities"),
            Category(name="Housing", description="Rent, mortgage, and utilities"),
            Category(name="Health", description="Medical expenses and health insurance")
        ]
        db.add_all(categories)
        db.commit()

        # Refresh to get IDs
        for cat in categories:
            db.refresh(cat)

        # Create accounts
        accounts = [
            Account(name="Cash", initial_balance=Decimal("500.00")),
            Account(name="Bank Account", initial_balance=Decimal("2500.00")),
            Account(name="Credit Card", initial_balance=Decimal("0.00"))
        ]
        db.add_all(accounts)
        db.commit()

        # Refresh to get IDs
        for acc in accounts:
            db.refresh(acc)

        # Create tags
        tags = [
            Tag(name="Essential"),
            Tag(name="Luxury"),
            Tag(name="Work"),
            Tag(name="Personal")
        ]
        db.add_all(tags)
        db.commit()

        # Refresh to get IDs
        for tag in tags:
            db.refresh(tag)

        # Create expenses
        today = date.today()
        expenses = [
            Expense(
                amount=Decimal("35.50"),
                date=today - timedelta(days=2),
                description="Grocery shopping",
                category_id=categories[0].id,  # Food
                account_id=accounts[1].id  # Bank Account
            ),
            Expense(
                amount=Decimal("12.00"),
                date=today - timedelta(days=1),
                description="Bus ticket",
                category_id=categories[1].id,  # Transportation
                account_id=accounts[0].id  # Cash
            ),
            Expense(
                amount=Decimal("50.00"),
                date=today,
                description="Movie and dinner",
                category_id=categories[2].id,  # Entertainment
                account_id=accounts[2].id  # Credit Card
            ),
            Expense(
                amount=Decimal("150.00"),
                date=today - timedelta(days=5),
                description="Electric bill",
                category_id=categories[3].id,  # Housing
                account_id=accounts[1].id  # Bank Account
            )
        ]
        db.add_all(expenses)
        db.commit()

        # Add tags to expenses
        expenses[0].tags.append(tags[0])  # Essential
        expenses[1].tags.append(tags[2])  # Work
        expenses[2].tags.append(tags[1])  # Luxury
        expenses[2].tags.append(tags[3])  # Personal
        expenses[3].tags.append(tags[0])  # Essential
        db.commit()

        # Create budgets for current month
        current_month = today.month
        current_year = today.year
        budgets = [
            Budget(
                category_id=categories[0].id,  # Food
                year=current_year,
                month=current_month,
                amount=Decimal("300.00")
            ),
            Budget(
                category_id=categories[1].id,  # Transportation
                year=current_year,
                month=current_month,
                amount=Decimal("150.00")
            ),
            Budget(
                category_id=categories[2].id,  # Entertainment
                year=current_year,
                month=current_month,
                amount=Decimal("200.00")
            ),
            Budget(
                category_id=categories[3].id,  # Housing
                year=current_year,
                month=current_month,
                amount=Decimal("1000.00")
            )
        ]
        db.add_all(budgets)
        db.commit()

        # Create recurring expenses
        recurring_expenses = [
            RecurringExpense(
                name="Monthly Rent",
                amount=Decimal("800.00"),
                category_id=categories[3].id,  # Housing
                interval="monthly",
                next_date=date(current_year, current_month + 1 if current_month < 12 else 1, 1),
                end_date=None
            ),
            RecurringExpense(
                name="Netflix Subscription",
                amount=Decimal("15.99"),
                category_id=categories[2].id,  # Entertainment
                interval="monthly",
                next_date=date(current_year, current_month + 1 if current_month < 12 else 1, 15),
                end_date=None
            ),
            RecurringExpense(
                name="Gym Membership",
                amount=Decimal("50.00"),
                category_id=categories[4].id,  # Health
                interval="monthly",
                next_date=date(current_year, current_month + 1 if current_month < 12 else 1, 5),
                end_date=date(current_year + 1, current_month, 5)  # 1 year from now
            )
        ]
        db.add_all(recurring_expenses)
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
