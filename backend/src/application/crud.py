import uuid

from sqlalchemy.orm import Session

from src.domain import models
from src.application import schemas


def _check_user_exists(db: Session, user_id: str):
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise ValueError(f"User with ID {user_id} not found.")

def _check_group_exists(db: Session, group_id: str):
    if not db.query(models.Group).filter(models.Group.id == group_id).first():
        raise ValueError(f"Group with ID {group_id} not found.")

def _check_expense_category_exists(db: Session, category_id: int):
    if not db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == category_id).first():
        raise ValueError(f"Expense category with ID {category_id} not found.")

def _check_credit_card_exists(db: Session, credit_card_id: int):
    if not db.query(models.CreditCard).filter(models.CreditCard.id == credit_card_id).first():
        raise ValueError(f"Credit card with ID {credit_card_id} not found.")

def _check_recurring_expense_exists(db: Session, recurring_expense_id: int):
    if not db.query(models.RecurringExpense).filter(models.RecurringExpense.id == recurring_expense_id).first():
        raise ValueError(f"Recurring expense with ID {recurring_expense_id} not found.")

def _check_income_category_exists(db: Session, category_id: int):
    if not db.query(models.IncomeCategory).filter(models.IncomeCategory.id == category_id).first():
        raise ValueError(f"Income category with ID {category_id} not found.")


# --- User CRUD ---
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        id=user.id,
        username=user.username,
        email=user.email,
        display_name=user.display_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# --- Group CRUD ---
def get_group(db: Session, group_id: str):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def create_group(db: Session, group: schemas.GroupCreate, owner_id: str):
    db_group = models.Group(**group.dict(), id=str(uuid.uuid4()))
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    # Add the owner as the first member of the group
    db_user = get_user(db, owner_id)
    if db_user:
        db_group.members.append(db_user)
        db.commit()
    return db_group


def update_group(db: Session, group_id: str, group_update: schemas.GroupUpdate):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group:
        update_data = group_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_group, key, value)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: str):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
    return db_group


# --- Credit Card CRUD ---

def get_credit_card(db: Session, credit_card_id: int):
    return (
        db.query(models.CreditCard)
        .filter(models.CreditCard.id == credit_card_id)
        .first()
    )


def get_credit_cards_by_user(db: Session, user_id: str):
    return (
        db.query(models.CreditCard).filter(models.CreditCard.owner_id == user_id).all()
    )


def create_credit_card(db: Session, credit_card: schemas.CreditCardCreate):
    db_credit_card = models.CreditCard(**credit_card.dict())
    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    return db_credit_card


def update_credit_card(db: Session, credit_card_id: int, credit_card_update: schemas.CreditCardUpdate):
    db_credit_card = db.query(models.CreditCard).filter(models.CreditCard.id == credit_card_id).first()
    if db_credit_card:
        update_data = credit_card_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_credit_card, key, value)
        db.add(db_credit_card)
        db.commit()
        db.refresh(db_credit_card)
    return db_credit_card


def delete_credit_card(db: Session, credit_card_id: int):
    db_credit_card = db.query(models.CreditCard).filter(models.CreditCard.id == credit_card_id).first()
    if db_credit_card:
        db.delete(db_credit_card)
        db.commit()
    return db_credit_card


# --- Expense CRUD ---
def _check_expense_related_ids(db: Session, expense_data: schemas.ExpenseCreate | schemas.ExpenseUpdate):
    if expense_data.owner_id and not db.query(models.User).filter(models.User.id == expense_data.owner_id).first():
        raise ValueError(f"Owner with ID {expense_data.owner_id} not found.")
    if expense_data.group_id and not db.query(models.Group).filter(models.Group.id == expense_data.group_id).first():
        raise ValueError(f"Group with ID {expense_data.group_id} not found.")
    if expense_data.category_id and not db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == expense_data.category_id).first():
        raise ValueError(f"Expense category with ID {expense_data.category_id} not found.")
    if expense_data.credit_card_id and not db.query(models.CreditCard).filter(models.CreditCard.id == expense_data.credit_card_id).first():
        raise ValueError(f"Credit card with ID {expense_data.credit_card_id} not found.")
    if expense_data.recurring_expense_id and not db.query(models.RecurringExpense).filter(models.RecurringExpense.id == expense_data.recurring_expense_id).first():
        raise ValueError(f"Recurring expense with ID {expense_data.recurring_expense_id} not found.")
    
    if isinstance(expense_data, schemas.ExpenseCreate):
        for split_data in expense_data.splits:
            if not db.query(models.User).filter(models.User.id == split_data.user_id).first():
                raise ValueError(f"User with ID {split_data.user_id} in split not found.")

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def get_expenses_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Expense)
        .filter(models.Expense.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    _check_user_exists(db, expense.owner_id)
    if expense.group_id:
        _check_group_exists(db, expense.group_id)
    if expense.category_id:
        _check_expense_category_exists(db, expense.category_id)
    if expense.credit_card_id:
        _check_credit_card_exists(db, expense.credit_card_id)
    if expense.recurring_expense_id:
        _check_recurring_expense_exists(db, expense.recurring_expense_id)
    
    for split_data in expense.splits:
        _check_user_exists(db, split_data.user_id)

    total_split_amount = sum(split.amount for split in expense.splits)
    if total_split_amount != expense.total_amount:
        raise ValueError(
            "The sum of split amounts must equal the total expense amount."
        )

    db_expense = models.Expense(
        human_readable_id=f"exp_{uuid.uuid4().hex[:8]}",
        description=expense.description,
        total_amount=expense.total_amount,
        due_date=expense.due_date,
        owner_id=expense.owner_id,
        group_id=expense.group_id,
        category_id=expense.category_id,
        credit_card_id=expense.credit_card_id,
        recurring_expense_id=expense.recurring_expense_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    for split_data in expense.splits:
        db_split = models.ExpenseSplit(
            expense_id=db_expense.id,
            user_id=split_data.user_id,
            amount=split_data.amount,
        )
        db.add(db_split)

    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense_update: schemas.ExpenseUpdate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        return None

    if expense_update.owner_id:
        _check_user_exists(db, expense_update.owner_id)
    if expense_update.group_id:
        _check_group_exists(db, expense_update.group_id)
    if expense_update.category_id:
        _check_expense_category_exists(db, expense_update.category_id)
    if expense_update.credit_card_id:
        _check_credit_card_exists(db, expense_update.credit_card_id)
    if expense_update.recurring_expense_id:
        _check_recurring_expense_exists(db, expense_update.recurring_expense_id)

    update_data = expense_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense


# --- Expense Category CRUD ---
def get_expense_category(db: Session, category_id: int):
    return (
        db.query(models.ExpenseCategory)
        .filter(models.ExpenseCategory.id == category_id)
        .first()
    )


def get_expense_category_by_name(db: Session, name: str):
    return (
        db.query(models.ExpenseCategory)
        .filter(models.ExpenseCategory.name == name)
        .first()
    )


def get_expense_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExpenseCategory).offset(skip).limit(limit).all()


def create_expense_category(db: Session, category: schemas.ExpenseCategoryCreate):
    db_category = models.ExpenseCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_expense_category(db: Session, category_id: int, category_update: schemas.ExpenseCategoryUpdate):
    db_category = db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == category_id).first()
    if db_category:
        update_data = category_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_expense_category(db: Session, category_id: int):
    db_category = db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# --- Income CRUD ---
def get_income(db: Session, income_id: int):
    return db.query(models.Income).filter(models.Income.id == income_id).first()


def get_incomes_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Income)
        .filter(models.Income.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_income(db: Session, income: schemas.IncomeCreate):
    _check_user_exists(db, income.owner_id)
    if income.category_id:
        _check_income_category_exists(db, income.category_id)

    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def update_income(db: Session, income_id: int, income_update: schemas.IncomeUpdate):
    db_income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not db_income:
        return None
    
    if income_update.owner_id:
        _check_user_exists(db, income_update.owner_id)
    if income_update.category_id:
        _check_income_category_exists(db, income_update.category_id)

    update_data = income_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_income, key, value)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def delete_income(db: Session, income_id: int):
    db_income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if db_income:
        db.delete(db_income)
        db.commit()
    return db_income


# --- Recurring Expense CRUD ---
def get_recurring_expense(db: Session, recurring_expense_id: int):
    return (
        db.query(models.RecurringExpense)
        .filter(models.RecurringExpense.id == recurring_expense_id)
        .first()
    )


def get_recurring_expenses_by_user(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.RecurringExpense)
        .filter(models.RecurringExpense.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_recurring_expense(
    db: Session, recurring_expense: schemas.RecurringExpenseCreate
):
    # Basic validation
    total_split_amount = sum(split.amount for split in recurring_expense.splits)
    if total_split_amount != recurring_expense.total_amount:
        raise ValueError(
            "The sum of split amounts must equal the total recurring expense amount."
        )

    db_recurring_expense = models.RecurringExpense(
        owner_id=recurring_expense.owner_id,
        group_id=recurring_expense.group_id,
        credit_card_id=recurring_expense.credit_card_id,
        description=recurring_expense.description,
        total_amount=recurring_expense.total_amount,
        installments=recurring_expense.installments,
        start_date=recurring_expense.start_date,
        end_date=recurring_expense.end_date,
        frequency=recurring_expense.frequency,
    )
    db.add(db_recurring_expense)
    db.commit()
    db.refresh(db_recurring_expense)

    # Create the splits
    for split_data in recurring_expense.splits:
        db_split = models.RecurringExpenseSplit(
            recurring_expense_id=db_recurring_expense.id,
            user_id=split_data.user_id,
            amount=split_data.amount,
        )
        db.add(db_split)

    db.commit()
    db.refresh(db_recurring_expense)
    return db_recurring_expense


def update_recurring_expense(db: Session, recurring_expense_id: int, recurring_expense_update: schemas.RecurringExpenseUpdate):
    db_recurring_expense = db.query(models.RecurringExpense).filter(models.RecurringExpense.id == recurring_expense_id).first()
    if db_recurring_expense:
        update_data = recurring_expense_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_recurring_expense, key, value)
        db.add(db_recurring_expense)
        db.commit()
        db.refresh(db_recurring_expense)
    return db_recurring_expense


def delete_recurring_expense(db: Session, recurring_expense_id: int):
    db_recurring_expense = db.query(models.RecurringExpense).filter(models.RecurringExpense.id == recurring_expense_id).first()
    if db_recurring_expense:
        db.delete(db_recurring_expense)
        db.commit()
    return db_recurring_expense

