from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.order_item import OrderItemCreate, OrderItemUpdate

def get_order_items(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM OrderItems LIMIT :limit OFFSET :skip"), {"limit": limit, "skip": skip}).mappings()
    return [dict(row) for row in result]

def get_order_item(db: Session, order_id: int, product_id: int):
    result = db.execute(
        text("SELECT * FROM OrderItems WHERE order_id = :order_id AND product_id = :product_id"),
        {"order_id": order_id, "product_id": product_id}
    ).first()
    return dict(result) if result else None

def create_order_item(db: Session, item: OrderItemCreate):
    db.execute(
        text("INSERT INTO OrderItems (order_id, product_id, quantity, price) VALUES (:order_id, :product_id, :quantity, :price)"),
        {
            "order_id": item.order_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        }
    )
    db.commit()
    return {"message": "Order item created successfully"}

def update_order_item(db: Session, order_id: int, product_id: int, item: OrderItemUpdate):
    db.execute(
        text("UPDATE OrderItems SET quantity = :quantity, price = :price WHERE order_id = :order_id AND product_id = :product_id"),
        {
            "quantity": item.quantity,
            "price": item.price,
            "order_id": order_id,
            "product_id": product_id
        }
    )
    db.commit()
    return {"message": "Order item updated successfully"}

def delete_order_item(db: Session, order_id: int, product_id: int):
    db.execute(
        text("DELETE FROM OrderItems WHERE order_id = :order_id AND product_id = :product_id"),
        {"order_id": order_id, "product_id": product_id}
    )
    db.commit()
    return {"message": "Order item deleted successfully"}
