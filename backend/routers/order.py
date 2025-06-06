from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from schemas.order import OrderCreate, OrderUpdate, Order, OrderCreateWithItems
from crud import order as crud_order
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all orders
@router.get("/", response_model=list[Order])
def get_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_order.get_orders(db)

# Get order by ID
@router.get("/{order_id}", response_model=Order)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Get orders by user ID
@router.get("/user/{user_id}", response_model=list[Order])
def get_orders_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_order.get_orders_by_user_id(db, user_id)

# Create a new order
@router.post("/", response_model=dict)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_order.create_order(db, order)

@router.post("/with-items")
def create_order_with_items(order: OrderCreateWithItems, db: Session = Depends(get_db)):
    return crud_order.create_order_with_items(db, order)


# Update an existing order
@router.patch("/{order_id}", response_model=dict)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_order.get_order_by_id(db, order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud_order.update_order(db, order_id, order)


# Delete an order
@router.delete("/{order_id}", response_model=dict)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_order.get_order_by_id(db, order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.delete_order(db, order_id)
    return {"message": "Order deleted successfully"}
