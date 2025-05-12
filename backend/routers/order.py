from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from models.database import SessionLocal
from schemas.order import OrderCreate, OrderUpdate, Order
from crud import order as crud_order

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all orders
@router.get("/", response_model=list[Order])
def get_orders(db: Session = Depends(get_db)):
    return crud_order.get_orders(db)

# Get order by ID
@router.get("/{order_id}", response_model=Order)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Create a new order
@router.post("/", response_model=dict)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order)

# Update an existing order
@router.put("/{order_id}", response_model=dict)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    existing = crud_order.get_order_by_id(db, order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.update_order(db, order_id, order)
    return {"message": "Order updated successfully"}

# Delete an order
@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    existing = crud_order.get_order_by_id(db, order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.delete_order(db, order_id)
    return {"message": "Order deleted successfully"}