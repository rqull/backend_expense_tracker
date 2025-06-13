from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from fastapi import HTTPException
from decimal import Decimal

from . import models, schemas

# Category CRUD operations
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category with this name already exists")

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category with this name already exists")

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}

# Expense CRUD operations
def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).options(
        joinedload(models.Expense.category),
        joinedload(models.Expense.account),
        joinedload(models.Expense.tags)
    ).filter(models.Expense.id == expense_id).first()

def get_expenses(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    query = db.query(models.Expense).options(
        joinedload(models.Expense.category),
        joinedload(models.Expense.account),
        joinedload(models.Expense.tags)
    )

    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    if account_id:
        query = query.filter(models.Expense.account_id == account_id)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)

    return query.order_by(models.Expense.date.desc()).offset(skip).limit(limit).all()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    # Verify category_id exists
    if not get_category(db, expense.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    # Verify account_id if provided
    if expense.account_id and not get_account(db, expense.account_id):
        raise HTTPException(status_code=400, detail="Account not found")

    # Extract tag_ids for many-to-many relationship handling
    tag_ids = expense.tag_ids or []
    expense_data = expense.dict(exclude={"tag_ids"})

    db_expense = models.Expense(**expense_data)
    db.add(db_expense)
    db.flush()  # To get the expense ID before committing

    # Add tags if provided
    if tag_ids:
        _add_tags_to_expense(db, db_expense.id, tag_ids)

    db.commit()
    db.refresh(db_expense)
    return db_expense

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseUpdate):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Verify category_id if provided
    if expense.category_id and not get_category(db, expense.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    # Verify account_id if provided
    if expense.account_id is not None and expense.account_id != 0 and not get_account(db, expense.account_id):
        raise HTTPException(status_code=400, detail="Account not found")

    # Handle tag updates if provided
    tag_ids = None
    if hasattr(expense, "tag_ids"):
        tag_ids = expense.tag_ids

    # Update expense fields
    update_data = expense.dict(exclude={"tag_ids"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    # Update tags if provided
    if tag_ids is not None:
        # Clear existing tags
        db.query(models.ExpenseTag).filter(models.ExpenseTag.expense_id == expense_id).delete()
        # Add new tags
        if tag_ids:
            _add_tags_to_expense(db, expense_id, tag_ids)

    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

# Helper function to add tags to an expense
def _add_tags_to_expense(db: Session, expense_id: int, tag_ids: List[int]):
    for tag_id in tag_ids:
        # Verify tag exists
        if not get_tag(db, tag_id):
            raise HTTPException(status_code=400, detail=f"Tag with id {tag_id} not found")
        # Add the relationship
        db_expense_tag = models.ExpenseTag(expense_id=expense_id, tag_id=tag_id)
        db.add(db_expense_tag)

# Budget CRUD operations
def get_budget(db: Session, budget_id: int):
    return db.query(models.Budget).options(
        joinedload(models.Budget.category)
    ).filter(models.Budget.id == budget_id).first()

def get_budgets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Budget).options(
        joinedload(models.Budget.category)
    ).offset(skip).limit(limit).all()

def create_budget(db: Session, budget: schemas.BudgetCreate):
    # Verify category exists
    if not get_category(db, budget.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    # Check for existing budget for this category/year/month
    existing = db.query(models.Budget).filter(
        models.Budget.category_id == budget.category_id,
        models.Budget.year == budget.year,
        models.Budget.month == budget.month
    ).first()

    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Budget for category_id {budget.category_id} for {budget.year}-{budget.month} already exists"
        )

    db_budget = models.Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, budget: schemas.BudgetUpdate):
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    # Verify category if changing
    if budget.category_id and not get_category(db, budget.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    # Check if update would create a duplicate
    update_data = budget.dict(exclude_unset=True)

    # If any of these fields are being updated, check for uniqueness constraint
    if any(key in update_data for key in ["category_id", "year", "month"]):
        # Get the new values, defaulting to current values if not being updated
        new_category_id = update_data.get("category_id", db_budget.category_id)
        new_year = update_data.get("year", db_budget.year)
        new_month = update_data.get("month", db_budget.month)

        # Check for existing budget with these values
        existing = db.query(models.Budget).filter(
            models.Budget.category_id == new_category_id,
            models.Budget.year == new_year,
            models.Budget.month == new_month,
            models.Budget.id != budget_id  # Exclude this budget
        ).first()

        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Budget for category_id {new_category_id} for {new_year}-{new_month} already exists"
            )

    # Update budget fields
    for key, value in update_data.items():
        setattr(db_budget, key, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int):
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(db_budget)
    db.commit()
    return {"message": "Budget deleted successfully"}

def get_budget_status(db: Session, year: int, month: int):
    # Get all budgets for the specified month and year
    budgets = db.query(
        models.Budget,
        models.Category.name.label("category_name")
    ).join(
        models.Category,
        models.Budget.category_id == models.Category.id
    ).filter(
        models.Budget.year == year,
        models.Budget.month == month
    ).all()

    # For each budget, calculate how much has been spent
    result = []
    for budget, category_name in budgets:
        # Calculate total spent for this category in this month/year
        total_spent = db.query(func.sum(models.Expense.amount)).filter(
            models.Expense.category_id == budget.category_id,
            extract('year', models.Expense.date) == year,
            extract('month', models.Expense.date) == month
        ).scalar() or 0

        # Calculate percentage spent
        percent = (float(total_spent) / float(budget.amount)) * 100 if budget.amount > 0 else 0

        # Add to result
        result.append(schemas.BudgetStatus(
            category_id=budget.category_id,
            category_name=category_name,
            budget_amount=budget.amount,
            total_spent=total_spent,
            percent=percent
        ))

    return result

# Account CRUD operations
def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    try:
        db.commit()
        db.refresh(db_account)
        return db_account
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Account with this name already exists")

def update_account(db: Session, account_id: int, account: schemas.AccountUpdate):
    db_account = get_account(db, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_data = account.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)

    try:
        db.commit()
        db.refresh(db_account)
        return db_account
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Account with this name already exists")

def delete_account(db: Session, account_id: int):
    db_account = get_account(db, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(db_account)
    db.commit()
    return {"message": "Account deleted successfully"}

# Tag CRUD operations
def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    try:
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tag with this name already exists")

def update_tag(db: Session, tag_id: int, tag: schemas.TagUpdate):
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    update_data = tag.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)

    try:
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tag with this name already exists")

def delete_tag(db: Session, tag_id: int):
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}

# RecurringExpense CRUD operations
def get_recurring_expense(db: Session, recurring_id: int):
    return db.query(models.RecurringExpense).options(
        joinedload(models.RecurringExpense.category)
    ).filter(models.RecurringExpense.id == recurring_id).first()

def get_recurring_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RecurringExpense).options(
        joinedload(models.RecurringExpense.category)
    ).offset(skip).limit(limit).all()

def create_recurring_expense(db: Session, recurring: schemas.RecurringExpenseCreate):
    # Verify category exists
    if not get_category(db, recurring.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    db_recurring = models.RecurringExpense(**recurring.dict())
    db.add(db_recurring)
    db.commit()
    db.refresh(db_recurring)
    return db_recurring

def update_recurring_expense(db: Session, recurring_id: int, recurring: schemas.RecurringExpenseUpdate):
    db_recurring = get_recurring_expense(db, recurring_id)
    if not db_recurring:
        raise HTTPException(status_code=404, detail="Recurring expense not found")

    # Verify category if changing
    if recurring.category_id and not get_category(db, recurring.category_id):
        raise HTTPException(status_code=400, detail="Category not found")

    update_data = recurring.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recurring, key, value)

    db.commit()
    db.refresh(db_recurring)
    return db_recurring

def delete_recurring_expense(db: Session, recurring_id: int):
    db_recurring = get_recurring_expense(db, recurring_id)
    if not db_recurring:
        raise HTTPException(status_code=404, detail="Recurring expense not found")

    db.delete(db_recurring)
    db.commit()
    return {"message": "Recurring expense deleted successfully"}

def generate_recurring_expenses(db: Session, date_today: Optional[date] = None):
    if date_today is None:
        date_today = date.today()

    # Find all recurring expenses where next_date <= today and end_date is None or end_date >= today
    due_recurring = db.query(models.RecurringExpense).filter(
        models.RecurringExpense.next_date <= date_today,
        (models.RecurringExpense.end_date.is_(None) | 
         (models.RecurringExpense.end_date >= date_today))
    ).all()

    generated_expenses = []

    for recurring in due_recurring:
        # Create a new expense
        expense = models.Expense(
            amount=recurring.amount,
            date=recurring.next_date,
            description=f"Auto-generated from recurring: {recurring.name}",
            category_id=recurring.category_id
        )
        db.add(expense)
        db.flush()  # To get the new expense ID
        generated_expenses.append(expense)

        # Update the next_date based on interval
        recurring.next_date = _calculate_next_date(recurring.next_date, recurring.interval)

        # If new next_date is beyond end_date, mark it as expired or handle appropriately
        if recurring.end_date and recurring.next_date > recurring.end_date:
            # Option 1: Delete the recurring expense
            # db.delete(recurring)

            # Option 2: Set next_date to a date beyond end_date to prevent future generation
            # but keep the record for reference
            recurring.next_date = recurring.end_date + timedelta(days=1)

    db.commit()
    # Refresh all expenses to get their complete data with relationships
    for expense in generated_expenses:
        db.refresh(expense)

    return generated_expenses

# Helper function to calculate next date based on interval
def _calculate_next_date(current_date: date, interval: str) -> date:
    if interval.lower() == "daily":
        return current_date + timedelta(days=1)
    elif interval.lower() == "weekly":
        return current_date + timedelta(days=7)
    elif interval.lower() == "biweekly":
        return current_date + timedelta(days=14)
    elif interval.lower() == "monthly":
        # Handle month rollover properly
        month = current_date.month + 1
        year = current_date.year

        if month > 12:
            month = 1
            year += 1

        # Handle cases where the day might not exist in the next month
        day = min(current_date.day, _get_days_in_month(year, month))

        return date(year, month, day)
    elif interval.lower() == "quarterly":
        # Add 3 months
        month = current_date.month + 3
        year = current_date.year

        if month > 12:
            month = month - 12
            year += 1

        day = min(current_date.day, _get_days_in_month(year, month))

        return date(year, month, day)
    elif interval.lower() == "yearly" or interval.lower() == "annually":
        return date(current_date.year + 1, current_date.month, current_date.day)
    else:
        # Default to monthly if interval is not recognized
        return _calculate_next_date(current_date, "monthly")

# Helper function to get the number of days in a month
def _get_days_in_month(year: int, month: int) -> int:
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        # Check for leap year
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        else:
            return 28
    else:
        return 31

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}