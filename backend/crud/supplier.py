from sqlalchemy.orm import Session
from schemas.supplier import SupplierCreate, SupplierUpdate
from sqlalchemy import text

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    query = text("SELECT * FROM Suppliers LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip}).mappings()
    return [dict(row) for row in result]

def get_supplier_by_id(db: Session, supplier_id: int):
    query = text("SELECT * FROM Suppliers WHERE id = :supplier_id")
    result = db.execute(query, {"supplier_id": supplier_id}).mappings().first()
    return dict(result) if result else None

def create_supplier(db: Session, supplier: SupplierCreate):
    query = text("""
        INSERT INTO Suppliers (name, phone_number, email, address)
        VALUES (:name, :phone_number, :email, :address)
    """)
    db.execute(query, supplier.dict())
    db.commit()

    # Get the newly inserted supplier (assuming AUTO_INCREMENT `id`)
    result = db.execute(text("SELECT * FROM Suppliers ORDER BY id DESC LIMIT 1")).mappings().first()
    return dict(result)

def update_supplier(db: Session, supplier_id: int, supplier_data: SupplierUpdate):
    existing = get_supplier_by_id(db, supplier_id)
    if not existing:
        return None

    update_fields = supplier_data.dict(exclude_unset=True)
    set_clause = ", ".join(f"{key} = :{key}" for key in update_fields.keys())
    update_fields["supplier_id"] = supplier_id

    query = text(f"""
        UPDATE Suppliers
        SET {set_clause}
        WHERE id = :supplier_id
    """)
    db.execute(query, update_fields)
    db.commit()

    return get_supplier_by_id(db, supplier_id)

def delete_supplier(db: Session, supplier_id: int):
    existing = get_supplier_by_id(db, supplier_id)
    if not existing:
        return None

    db.execute(text("DELETE FROM Suppliers WHERE id = :supplier_id"), {"supplier_id": supplier_id})
    db.commit()
    return {"message": "Supplier deleted successfully"}
