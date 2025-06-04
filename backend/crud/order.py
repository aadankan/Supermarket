import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderCreateWithItems, OrderUpdate

# Get all orders
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM orders")).mappings()
    return [dict(row) for row in result]

# Get a specific order by ID
def get_order_by_id(db: Session, order_id: int):
    result = db.execute(text("SELECT * FROM orders WHERE id = :id"), {"id": order_id}).first()
    return dict(result) if result else None

# Create a new order
def create_order(db: Session, order: OrderCreate):
    db.execute(
        text("INSERT INTO orders (user_id, order_date, status) VALUES (:user_id, :order_date, :status)"),
        {
            "user_id": order.user_id,
            "order_date": order.order_date,
            "status": order.status
        }
    )
    db.commit()
    return {"message": "Order created successfully"}

def create_order_with_items(db: Session, order_data: OrderCreateWithItems):
    db.execute(
        text("""
            INSERT INTO Orders (user_id, order_date, status, shipping_address_id, billing_address_id)
            VALUES (:user_id, :order_date, :status, :shipping_address_id, :billing_address_id)
        """),
        {
            "user_id": order_data.user_id,
            "order_date": order_data.order_date or datetime.utcnow(),
            "status": order_data.status or "pending",
            "shipping_address_id": order_data.shipping_address_id,
            "billing_address_id": order_data.billing_address_id,
        }
    )
    order_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()

    for item in order_data.items:
        db.execute(
            text("""
                INSERT INTO OrderItems (order_id, product_id, quantity, price)
                VALUES (:order_id, :product_id, :quantity, :price)
            """),
            {
                "order_id": order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
            }
        )

        db.execute(
            text("""
                UPDATE Inventory
                SET quantity = quantity - :quantity
                WHERE product_id = :product_id AND quantity >= :quantity
            """),
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            }
        )

    db.commit()
    return {"message": "Order created successfully", "order_id": order_id}

# Update an existing order
def update_order(db: Session, order_id: int, order_data: OrderUpdate):
    db.execute(
        text("UPDATE orders SET user_id = :user_id, order_date = :order_date, status = :status WHERE id = :id"),
        {
            "user_id": order_data.user_id,
            "order_date": order_data.order_date,
            "status": order_data.status,
            "id": order_id
        }
    )
    db.commit()
    return {"message": "Order updated successfully"}

# Delete an order
def delete_order(db: Session, order_id: int):
    db.execute(text("DELETE FROM orders WHERE id = :id"), {"id": order_id})
    db.commit()
    return {"message": "Order deleted successfully"}
