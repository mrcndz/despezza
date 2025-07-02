from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.RecurringExpense)
def create_recurring_expense(recurring_expense: schemas.RecurringExpenseCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_recurring_expense(db=db, recurring_expense=recurring_expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{recurring_expense_id}", response_model=schemas.RecurringExpense)
def read_recurring_expense(recurring_expense_id: int, db: Session = Depends(get_db)):
    db_recurring_expense = crud.get_recurring_expense(db, recurring_expense_id=recurring_expense_id)
    if db_recurring_expense is None:
        raise HTTPException(status_code=404, detail="Recurring Expense not found")
    return db_recurring_expense

@router.get("/user/{user_id}", response_model=List[schemas.RecurringExpense])
def read_recurring_expenses_by_user(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recurring_expenses = crud.get_recurring_expenses_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return recurring_expenses

@router.patch("/{recurring_expense_id}", response_model=schemas.RecurringExpense)
def update_recurring_expense(recurring_expense_id: int, recurring_expense: schemas.RecurringExpenseUpdate, db: Session = Depends(get_db)):
    db_recurring_expense = crud.get_recurring_expense(db, recurring_expense_id=recurring_expense_id)
    if db_recurring_expense is None:
        raise HTTPException(status_code=404, detail="Recurring Expense not found")
    return crud.update_recurring_expense(db=db, recurring_expense_id=recurring_expense_id, recurring_expense_update=recurring_expense)

@router.delete("/{recurring_expense_id}", response_model=schemas.RecurringExpense)
def delete_recurring_expense(recurring_expense_id: int, db: Session = Depends(get_db)):
    db_recurring_expense = crud.get_recurring_expense(db, recurring_expense_id=recurring_expense_id)
    if db_recurring_expense is None:
        raise HTTPException(status_code=404, detail="Recurring Expense not found")
    return crud.delete_recurring_expense(db=db, recurring_expense_id=recurring_expense_id)