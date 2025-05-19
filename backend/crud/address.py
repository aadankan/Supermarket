from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.address import AddressCreate, AddressUpdate

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("SELECT * FROM Addresses LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).mappings()
    return [dict(row) for row in result]

def get_address_by_id(db: Session, address_id: int):
    result = db.execute(
        text("SELECT * FROM Addresses WHERE id = :id"),
        {"id": address_id}
    ).first()
    return dict(result) if result else None

def create_address(db: Session, address: AddressCreate):
    result = db.execute(
        text("""
            INSERT INTO Addresses (user_id, street, city, postal_code, country, is_default, created_at)
            VALUES (:user_id, :street, :city, :postal_code, :country, :is_default, :created_at)
        """),
        {
            "user_id": address.user_id,
            "street": address.street,
            "city": address.city,
            "postal_code": address.postal_code,
            "country": address.country,
            "is_default": address.is_default,
            "created_at": address.created_at
        }
    )
    db.commit()
    return {"message": "Address created successfully", "address_id": result.lastrowid}

def update_address(db: Session, address_id: int, address_data: AddressUpdate):
    values = address_data.dict(exclude_unset=True)
    if not values:
        return {"message": "No data to update"}

    set_clause = ", ".join(f"{key} = :{key}" for key in values.keys())
    values["id"] = address_id

    db.execute(
        text(f"UPDATE Addresses SET {set_clause} WHERE id = :id"),
        values
    )
    db.commit()
    return {"message": "Address updated successfully"}

def set_default_address(db: Session, user_id: int, address_id: int):
    db.execute(
        text("UPDATE Addresses SET is_default = 0 WHERE user_id = :user_id"),
        {"user_id": user_id}
    )
    db.execute(
        text("UPDATE Addresses SET is_default = 1 WHERE id = :address_id"),
        {"address_id": address_id}
    )
    db.commit()
    return {"message": "Default address updated successfully"}

def get_default_address(db: Session, user_id: int):
    result = db.execute(
        text("SELECT * FROM Addresses WHERE user_id = :user_id AND is_default = 1"),
        {"user_id": user_id}
    ).first()
    return dict(result) if result else None

def delete_address(db: Session, address_id: int):
    result = db.execute(
        text("DELETE FROM Addresses WHERE id = :id"),
        {"id": address_id}
    )
    db.commit()
    if result.rowcount == 0:
        return {"error": "Address not found"}
    return {"message": "Address deleted successfully"}