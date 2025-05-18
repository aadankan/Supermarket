from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.transaction import TransactionCreate, TransactionUpdate

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM Transactions ORDER BY timestamp DESC LIMIT :limit OFFSET :skip"),
                        {"limit": limit, "skip": skip}).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, transaction_id: int):
    result = db.execute(text("SELECT * FROM Transactions WHERE id = :id"), {"id": transaction_id}).first()
    return dict(result) if result else None

def create_transaction(db: Session, transaction: TransactionCreate):
    db.execute(text("""
        INSERT INTO Transactions (product_id, change, transaction_type, timestamp, note)
        VALUES (:product_id, :change, :transaction_type, :timestamp, :note)
    """), transaction.dict())
    db.commit()
    return {"message": "Transaction created successfully"}

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db.execute(text("""
        UPDATE Transactions
        SET change = :change,
            transaction_type = :transaction_type,
            timestamp = :timestamp,
            note = :note
        WHERE id = :id
    """), {**transaction.dict(), "id": transaction_id})
    db.commit()
    return {"message": "Transaction updated successfully"}

def delete_transaction(db: Session, transaction_id: int):
    db.execute(text("DELETE FROM Transactions WHERE id = :id"), {"id": transaction_id})
    db.commit()
    return {"message": "Transaction deleted successfully"}
