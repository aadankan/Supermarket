from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import SessionLocal
from schemas.category import Category, CategoryCreate, CategoryUpdate
from crud import category as crud_category
from models.user import User as UserModel
from routers.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Category])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_category.get_categories(db, skip, limit)

@router.get("/{category_id}", response_model=Category)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    category = crud_category.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_category.create_category(db, category)

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_category.get_by_id(db, category_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_category.update_category(db, category_id, category)

@router.delete("/{category_id}", response_model=dict)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_category.get_by_id(db, category_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_category.delete_category(db, category_id)
