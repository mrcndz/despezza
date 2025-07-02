from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for the many-to-many relationship between users and groups
user_group_association = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("group_id", String, ForeignKey("groups.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Firebase UID
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owned_expenses = relationship(
        "Expense", foreign_keys="Expense.owner_id", back_populates="owner"
    )
    incomes = relationship("Income", back_populates="owner")
    groups = relationship(
        "Group", secondary=user_group_association, back_populates="members"
    )
    recurring_expenses = relationship(
        "RecurringExpense",
        back_populates="owner",
        foreign_keys="RecurringExpense.owner_id",
    )
    splits = relationship("ExpenseSplit", back_populates="user")
    recurring_splits = relationship("RecurringExpenseSplit", back_populates="user")
    credit_cards = relationship("CreditCard", back_populates="owner")


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    members = relationship(
        "User", secondary=user_group_association, back_populates="groups"
    )
    expenses = relationship("Expense", back_populates="group")
    recurring_expenses = relationship("RecurringExpense", back_populates="group")


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    closing_day = Column(Integer, nullable=False)  # Day of the month the bill closes
    due_day = Column(Integer, nullable=False)  # Day of the month the bill is due

    # Relationships
    owner = relationship("User", back_populates="credit_cards")
    expenses = relationship("Expense", back_populates="credit_card")
    recurring_expenses = relationship("RecurringExpense", back_populates="credit_card")


class RecurringExpense(Base):
    __tablename__ = "recurring_expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    credit_card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    description = Column(Text, nullable=False)
    total_amount = Column(Integer, nullable=False)
    installments = Column(Integer, nullable=False, default=1)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    frequency = Column(
        String, nullable=False, default="monthly"
    )  # e.g., 'monthly', 'weekly'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship(
        "User", back_populates="recurring_expenses", foreign_keys=[owner_id]
    )
    group = relationship("Group", back_populates="recurring_expenses")
    credit_card = relationship("CreditCard", back_populates="recurring_expenses")
    expenses = relationship("Expense", back_populates="recurring_expense")
    splits = relationship("RecurringExpenseSplit", back_populates="recurring_expense")


class RecurringExpenseSplit(Base):
    __tablename__ = "recurring_expense_splits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recurring_expense_id = Column(
        Integer, ForeignKey("recurring_expenses.id"), nullable=False
    )
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Amount per installment

    # Relationships
    recurring_expense = relationship("RecurringExpense", back_populates="splits")
    user = relationship("User", back_populates="recurring_splits")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    human_readable_id = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    recurring_expense_id = Column(
        Integer, ForeignKey("recurring_expenses.id"), nullable=True
    )
    credit_card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    description = Column(Text, nullable=True)
    total_amount = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship(
        "User", foreign_keys=[owner_id], back_populates="owned_expenses"
    )
    group = relationship("Group", back_populates="expenses")
    credit_card = relationship("CreditCard", back_populates="expenses")
    recurring_expense = relationship("RecurringExpense", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")
    category = relationship("ExpenseCategory", back_populates="expenses")


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    paid_at = Column(DateTime, nullable=True)

    # Relationships
    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="splits")


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    expenses = relationship("Expense", back_populates="category")


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)
    received_at = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("income_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="incomes")
    category = relationship("IncomeCategory", back_populates="incomes")


class IncomeCategory(Base):
    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    incomes = relationship("Income", back_populates="category")
