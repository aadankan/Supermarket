from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import SessionLocal
from schemas.user import User, UserCreate, UserUpdate
from crud import user as crud_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.put("/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    existing = crud_user.get_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, user_id, user)

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing = crud_user.get_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db, user_id)
