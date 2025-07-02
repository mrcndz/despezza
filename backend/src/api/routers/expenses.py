from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_expense(db=db, expense=expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.get("/user/{user_id}", response_model=List[schemas.Expense])
def read_expenses_by_user(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    expenses = crud.get_expenses_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return expenses

@router.patch("/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return crud.update_expense(db=db, expense_id=expense_id, expense_update=expense)

@router.delete("/{expense_id}", response_model=schemas.Expense)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return crud.delete_expense(db=db, expense_id=expense_id)