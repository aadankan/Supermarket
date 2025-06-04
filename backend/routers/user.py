from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import SessionLocal
from schemas.user import User, UserCreate, UserOut, UserUpdate, EmailRequest
from crud import user as crud_user
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/get-user-id")
def get_user_id_by_email(data: EmailRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"userId": user["id"]}

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    existing = crud_user.get_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, user_id, user_update)

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing = crud_user.get_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db, user_id)
