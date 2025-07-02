from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date

# --- Schemas for User and Group ---
class UserBase(BaseModel):
    username: str
    email: str
    display_name: Optional[str] = None

class UserCreate(UserBase):
    id: str # Firebase UID

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None

class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Group(GroupBase):
    id: str
    created_at: datetime
    members: List[User] = []

    class Config:
        orm_mode = True

# --- Schemas for Credit Card ---
class CreditCardBase(BaseModel):
    name: str
    closing_day: int = Field(..., gt=0, le=31)
    due_day: int = Field(..., gt=0, le=31)
    owner_id: str

class CreditCardCreate(CreditCardBase):
    pass

class CreditCardUpdate(BaseModel):
    name: Optional[str] = None
    closing_day: Optional[int] = Field(None, gt=0, le=31)
    due_day: Optional[int] = Field(None, gt=0, le=31)

class CreditCard(CreditCardBase):
    id: int

    class Config:
        orm_mode = True

# --- Schemas for Expenses ---

# ExpenseCategory
class ExpenseCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass

class ExpenseCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ExpenseCategory(ExpenseCategoryBase):
    id: int
    
    class Config:
        orm_mode = True

# ExpenseSplit
class ExpenseSplitBase(BaseModel):
    user_id: str
    amount: int

class ExpenseSplitCreate(ExpenseSplitBase):
    pass

class ExpenseSplit(ExpenseSplitBase):
    id: int
    paid_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Expense
class ExpenseBase(BaseModel):
    description: Optional[str] = None
    total_amount: int
    due_date: date
    owner_id: str
    group_id: Optional[str] = None
    category_id: Optional[int] = None
    credit_card_id: Optional[int] = None
    recurring_expense_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    splits: List[ExpenseSplitCreate]

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    total_amount: Optional[int] = None
    due_date: Optional[date] = None
    group_id: Optional[str] = None
    category_id: Optional[int] = None
    credit_card_id: Optional[int] = None
    recurring_expense_id: Optional[int] = None

class Expense(ExpenseBase):
    id: int
    human_readable_id: str
    created_at: datetime
    updated_at: datetime
    splits: List[ExpenseSplit] = []
    category: Optional[ExpenseCategory] = None

    class Config:
        orm_mode = True

# --- Schemas for Income ---

# IncomeCategory
class IncomeCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class IncomeCategoryCreate(IncomeCategoryBase):
    pass

class IncomeCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class IncomeCategory(IncomeCategoryBase):
    id: int

    class Config:
        orm_mode = True

# Income
class IncomeBase(BaseModel):
    owner_id: str
    description: Optional[str] = None
    amount: int
    received_at: date
    category_id: Optional[int] = None

class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[int] = None
    received_at: Optional[date] = None
    category_id: Optional[int] = None

class Income(IncomeBase):
    id: int
    created_at: datetime
    category: Optional[IncomeCategory] = None

    class Config:
        orm_mode = True

# --- Schemas for Recurring Expenses ---

# RecurringExpenseSplit
class RecurringExpenseSplitBase(BaseModel):
    user_id: str
    amount: int

class RecurringExpenseSplitCreate(RecurringExpenseSplitBase):
    pass

class RecurringExpenseSplit(RecurringExpenseSplitBase):
    id: int

    class Config:
        orm_mode = True

# RecurringExpense
class RecurringExpenseBase(BaseModel):
    owner_id: str
    group_id: Optional[str] = None
    credit_card_id: Optional[int] = None
    description: str
    total_amount: int
    installments: int = Field(1, gt=0)
    start_date: date
    end_date: Optional[date] = None
    frequency: str = "monthly"

class RecurringExpenseCreate(RecurringExpenseBase):
    splits: List[RecurringExpenseSplitCreate]

class RecurringExpenseUpdate(BaseModel):
    description: Optional[str] = None
    total_amount: Optional[int] = None
    installments: Optional[int] = Field(None, gt=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    frequency: Optional[str] = None
    group_id: Optional[str] = None
    credit_card_id: Optional[int] = None

class RecurringExpense(RecurringExpenseBase):
    id: int
    created_at: datetime
    splits: List[RecurringExpenseSplit] = []

    class Config:
        orm_mode = True
