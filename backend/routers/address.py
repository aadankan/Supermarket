from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import SessionLocal
from schemas.address import AddressBase, AddressCreate, AddressUpdate
from crud import address as crud_address
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[AddressBase])
def get_addresses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_address.get_addresses(db, skip=skip, limit=limit)

@router.get("/{address_id}", response_model=AddressBase)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    address = crud_address.get_address_by_id(db, address_id)
    if not address or address["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found or unauthorized")
    return address

@router.post("/", response_model=dict)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_address.create_address(db, address, current_user.id)

@router.put("/{address_id}", response_model=dict)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_address.get_address_by_id(db, address_id)
    if not existing or existing["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found or unauthorized")
    return crud_address.update_address(db, address_id, address)

@router.delete("/{address_id}", response_model=dict)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_address.get_address_by_id(db, address_id)
    if not existing or existing["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found or unauthorized")
    return crud_address.delete_address(db, address_id)

@router.put("/set-default/{user_id}/{address_id}", response_model=dict)
def set_default_address(
    user_id: int,
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    existing = crud_address.get_address_by_id(db, address_id)
    if not existing or existing["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Address not found for this user")
    return crud_address.set_default_address(db, user_id, address_id)

@router.get("/default/{user_id}", response_model=AddressBase | None)
def get_default_address(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    address = crud_address.get_default_address(db, user_id)
    if not address:
        raise HTTPException(status_code=404, detail="Default address not found")
    return address
