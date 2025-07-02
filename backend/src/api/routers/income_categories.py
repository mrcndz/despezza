from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.IncomeCategory)
def create_income_category(category: schemas.IncomeCategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_income_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Income category already exists")
    return crud.create_income_category(db=db, category=category)

@router.get("/", response_model=List[schemas.IncomeCategory])
def read_income_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_income_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.IncomeCategory)
def read_income_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_income_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Income category not found")
    return db_category

@router.patch("/{category_id}", response_model=schemas.IncomeCategory)
def update_income_category(category_id: int, category: schemas.IncomeCategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.get_income_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Income category not found")
    return crud.update_income_category(db=db, category_id=category_id, category_update=category)

@router.delete("/{category_id}", response_model=schemas.IncomeCategory)
def delete_income_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_income_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Income category not found")
    return crud.delete_income_category(db=db, category_id=category_id)
