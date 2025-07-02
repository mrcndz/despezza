from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.CreditCard)
def create_credit_card(credit_card: schemas.CreditCardCreate, db: Session = Depends(get_db)):
    return crud.create_credit_card(db=db, credit_card=credit_card)

@router.get("/{credit_card_id}", response_model=schemas.CreditCard)
def read_credit_card(credit_card_id: int, db: Session = Depends(get_db)):
    db_credit_card = crud.get_credit_card(db, credit_card_id=credit_card_id)
    if db_credit_card is None:
        raise HTTPException(status_code=404, detail="Credit Card not found")
    return db_credit_card

@router.get("/user/{user_id}", response_model=List[schemas.CreditCard])
def read_credit_cards_by_user(user_id: str, db: Session = Depends(get_db)):
    credit_cards = crud.get_credit_cards_by_user(db, user_id=user_id)
    return credit_cards

@router.patch("/{credit_card_id}", response_model=schemas.CreditCard)
def update_credit_card(credit_card_id: int, credit_card: schemas.CreditCardUpdate, db: Session = Depends(get_db)):
    db_credit_card = crud.get_credit_card(db, credit_card_id=credit_card_id)
    if db_credit_card is None:
        raise HTTPException(status_code=404, detail="Credit Card not found")
    return crud.update_credit_card(db=db, credit_card_id=credit_card_id, credit_card_update=credit_card)

@router.delete("/{credit_card_id}", response_model=schemas.CreditCard)
def delete_credit_card(credit_card_id: int, db: Session = Depends(get_db)):
    db_credit_card = crud.get_credit_card(db, credit_card_id=credit_card_id)
    if db_credit_card is None:
        raise HTTPException(status_code=404, detail="Credit Card not found")
    return crud.delete_credit_card(db=db, credit_card_id=credit_card_id)