from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import crud, schemas
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, owner_id: str, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group, owner_id=owner_id)

@router.get("/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/{group_id}", response_model=schemas.Group)
def read_group(group_id: str, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.patch("/{group_id}", response_model=schemas.Group)
def update_group(group_id: str, group: schemas.GroupUpdate, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.update_group(db=db, group_id=group_id, group_update=group)

@router.delete("/{group_id}", response_model=schemas.Group)
def delete_group(group_id: str, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.delete_group(db=db, group_id=group_id)