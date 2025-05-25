from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import order_item as crud_order_item
from schemas.order_item import OrderItem, OrderItemCreate, OrderItemUpdate
from models.database import SessionLocal
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[OrderItem])
def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_order_item.get_order_items(db, skip=skip, limit=limit)

@router.get("/{order_id}/{product_id}", response_model=OrderItem)
def get_item(
    order_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    item = crud_order_item.get_order_item(db, order_id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item

@router.post("/", response_model=dict)
def create_item(
    item: OrderItemCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_order_item.create_order_item(db, item)

@router.put("/{order_id}/{product_id}", response_model=dict)
def update_item(
    order_id: int,
    product_id: int,
    item: OrderItemUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_order_item.get_order_item(db, order_id, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order item not found")
    return crud_order_item.update_order_item(db, order_id, product_id, item)

@router.delete("/{order_id}/{product_id}", response_model=dict)
def delete_item(
    order_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_order_item.get_order_item(db, order_id, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order item not found")
    return crud_order_item.delete_order_item(db, order_id, product_id)
