from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

# Income Categories
@router.post("/categories/", response_model=schemas.IncomeCategory)
def create_income_category(category: schemas.IncomeCategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_income_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Income category already exists")
    return crud.create_income_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.IncomeCategory])
def read_income_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_income_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=schemas.IncomeCategory)
def read_income_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_income_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Income category not found")
    return db_category

# Incomes
@router.post("/", response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return crud.create_income(db=db, income=income)

@router.get("/{income_id}", response_model=schemas.Income)
def read_income(income_id: int, db: Session = Depends(get_db)):
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income

@router.get("/user/{user_id}", response_model=List[schemas.Income])
def read_incomes_by_user(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incomes = crud.get_incomes_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return incomes

@router.patch("/{income_id}", response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeUpdate, db: Session = Depends(get_db)):
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return crud.update_income(db=db, income_id=income_id, income_update=income)

@router.delete("/{income_id}", response_model=schemas.Income)
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return crud.delete_income(db=db, income_id=income_id)