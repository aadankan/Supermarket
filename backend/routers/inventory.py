from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import inventory as crud_inventory
from schemas.inventory import InventoryCreate, InventoryUpdate, InventoryOut
from models.database import SessionLocal
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all inventory
@router.get("/", response_model=list[InventoryOut])
def get_inventory(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user)
):
    return crud_inventory.get_inventory(db=db, skip=skip, limit=limit)

# Get inventory by product ID
@router.get("/{product_id}", response_model=InventoryOut)
def get_inventory_by_product_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_inventory.get_inventory_by_product_id(db=db, product_id=product_id)

# Create inventory entry
@router.post("/", response_model=InventoryOut)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_inventory.create_inventory(db=db, inventory=inventory)

# Update inventory entry
@router.put("/{product_id}", response_model=InventoryOut)
def update_inventory(
    product_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud_inventory.update_inventory(db=db, product_id=product_id, inventory_data=inventory_data)
    return crud_inventory.get_inventory_by_product_id(db=db, product_id=product_id)

# Delete inventory entry
@router.delete("/{product_id}", response_model=dict)
def delete_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_inventory.delete_inventory(db=db, product_id=product_id)
