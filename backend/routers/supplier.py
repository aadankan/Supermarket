from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import supplier as crud_supplier
from schemas.supplier import SupplierCreate, SupplierUpdate, SupplierOut
from models.database import SessionLocal
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all suppliers
@router.get("/", response_model=list[SupplierOut])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_supplier.get_suppliers(db=db, skip=skip, limit=limit)

# Get single supplier by ID
@router.get("/{supplier_id}", response_model=SupplierOut)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = crud_supplier.get_supplier_by_id(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

# Create new supplier (auth required)
@router.post("/", response_model=SupplierOut)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_supplier.create_supplier(db=db, supplier=supplier)

# Update supplier (auth required)
@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_supplier = crud_supplier.update_supplier(db=db, supplier_id=supplier_id, supplier_data=supplier_data)
    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated_supplier

# Delete supplier (auth required)
@router.delete("/{supplier_id}", response_model=dict)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = crud_supplier.delete_supplier(db=db, supplier_id=supplier_id)
    if not result:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return result
