from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from decimal import Decimal

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Account Schemas
class AccountBase(BaseModel):
    name: str
    initial_balance: Optional[Decimal] = Field(0, ge=0)

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    initial_balance: Optional[Decimal] = None

class Account(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Expense Schemas
class ExpenseBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    date: date
    description: Optional[str] = None
    category_id: int
    account_id: Optional[int] = None

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

class ExpenseCreate(ExpenseBase):
    tag_ids: Optional[List[int]] = None
    receipt_path: Optional[str] = None

class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    receipt_path: Optional[str] = None

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be positive')
        return v

class Expense(ExpenseBase):
    id: int
    receipt_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    category: Category
    account: Optional[Account] = None
    tags: List[Tag] = []

    class Config:
        orm_mode = True

# Budget Schemas
class BudgetBase(BaseModel):
    category_id: int
    year: int
    month: int
    amount: Decimal = Field(..., gt=0)

    @validator('month')
    def validate_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('Month must be between 1 and 12')
        return v

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    category_id: Optional[int] = None
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[Decimal] = None

    @validator('month')
    def validate_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError('Month must be between 1 and 12')
        return v

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be positive')
        return v

class Budget(BudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category

    class Config:
        orm_mode = True

# Budget Status Schema for the budget status endpoint
class BudgetStatus(BaseModel):
    category_id: int
    category_name: str
    budget_amount: Decimal
    total_spent: Decimal
    percent: float

# RecurringExpense Schemas
class RecurringExpenseBase(BaseModel):
    name: str
    amount: Decimal = Field(..., gt=0)
    category_id: int
    interval: str  # e.g., "monthly", "weekly"
    next_date: date
    end_date: Optional[date] = None

class RecurringExpenseCreate(RecurringExpenseBase):
    pass

class RecurringExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[Decimal] = None
    category_id: Optional[int] = None
    interval: Optional[str] = None
    next_date: Optional[date] = None
    end_date: Optional[date] = None

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be positive')
        return v

class RecurringExpense(RecurringExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category

    class Config:
        orm_mode = True