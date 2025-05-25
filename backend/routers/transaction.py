from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut
from crud import transaction as crud_transaction
from models.database import SessionLocal
from typing import List
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TransactionOut])
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_transaction.get_transactions(db, skip, limit)

@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud_transaction.get_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=dict)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return crud_transaction.create_transaction(db, transaction)

@router.put("/{transaction_id}", response_model=dict)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_transaction.get_by_id(db, transaction_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud_transaction.update_transaction(db, transaction_id, transaction)

@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    existing = crud_transaction.get_by_id(db, transaction_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud_transaction.delete_transaction(db, transaction_id)
