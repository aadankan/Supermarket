from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.inventory import InventoryCreate, InventoryUpdate

# Get all inventory items
def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM Inventory")).mappings()
    return [dict(row) for row in result]

# Get inventory by product ID
def get_inventory_by_product_id(db: Session, product_id: int):
    result = db.execute(text("SELECT * FROM Inventory WHERE product_id = :id"), {"id": product_id}).first()
    return dict(result) if result else None

# Create inventory entry
def create_inventory(db: Session, inventory: InventoryCreate):
    db.execute(
        text("INSERT INTO Inventory (product_id, quantity, location) VALUES (:product_id, :quantity, :location)"),
        {
            "product_id": inventory.product_id,
            "quantity": inventory.quantity,
            "location": inventory.location
        }
    )
    db.commit()
    return {"message": "Inventory created successfully"}

# Update an inventory entry
def update_inventory(db: Session, product_id: int, inventory_data: InventoryUpdate):
    db.execute(
        text("UPDATE Inventory SET quantity = :quantity, location = :location WHERE product_id = :product_id"),
        {
            "quantity": inventory_data.quantity,
            "location": inventory_data.location,
            "product_id": product_id
        }
    )
    db.commit()

# Delete an inventory entry
def delete_inventory(db: Session, product_id: int):
    db.execute(text("DELETE FROM Inventory WHERE product_id = :id"), {"id": product_id})
    db.commit()
    return {"message": "Inventory deleted successfully"}
