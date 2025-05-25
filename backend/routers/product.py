from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import SessionLocal
from schemas.product import Product, ProductCreate, ProductUpdate
from crud import product as crud_product
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip, limit)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=dict)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_product.create_product(db, product)

@router.put("/{product_id}", response_model=dict)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_product.get_by_id(db, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    crud_product.update(db, product_id, product)
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}", response_model=dict)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_product.get_by_id(db, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    crud_product.delete(db, product_id)
    return {"message": "Product deleted successfully"}
