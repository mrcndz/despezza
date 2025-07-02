from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ExpenseCategory)
def create_expense_category(category: schemas.ExpenseCategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_expense_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Expense category already exists")
    return crud.create_expense_category(db=db, category=category)

@router.get("/", response_model=List[schemas.ExpenseCategory])
def read_expense_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_expense_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.ExpenseCategory)
def read_expense_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_expense_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expense category not found")
    return db_category

@router.patch("/{category_id}", response_model=schemas.ExpenseCategory)
def update_expense_category(category_id: int, category: schemas.ExpenseCategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.get_expense_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expense category not found")
    return crud.update_expense_category(db=db, category_id=category_id, category_update=category)

@router.delete("/{category_id}", response_model=schemas.ExpenseCategory)
def delete_expense_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_expense_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expense category not found")
    return crud.delete_expense_category(db=db, category_id=category_id)
