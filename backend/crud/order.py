import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderCreateWithItems, OrderUpdate

# Get all orders
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM Orders")).mappings()
    return [dict(row) for row in result]

# Get a specific order by ID
def get_order_by_id(db: Session, order_id: int):
    result = db.execute(text("SELECT * FROM Orders WHERE id = :id"), {"id": order_id}).mappings().first()
    return dict(result) if result else None

# Create a new order
def create_order(db: Session, order: OrderCreate):
    db.execute(
        text("INSERT INTO Orders (user_id, order_date, status) VALUES (:user_id, :order_date, :status)"),
        {
            "user_id": order.user_id,
            "order_date": order.order_date,
            "status": order.status
        }
    )
    db.commit()
    return {"message": "Order created successfully"}

def get_orders_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Pobieranie zamówień użytkownika
    orders_result = db.execute(
        text("SELECT * FROM Orders WHERE user_id = :user_id ORDER BY order_date DESC LIMIT :skip, :limit"),
        {"user_id": user_id, "skip": skip, "limit": limit}
    ).mappings()

    orders = []
    for order_row in orders_result:
        order = dict(order_row)

        # Pobierz powiązane produkty w zamówieniu (OrderItems + Products)
        items_result = db.execute(
            text("""
                SELECT 
                    oi.product_id, 
                    oi.quantity, 
                    oi.price, 
                    p.name, 
                    p.image_url 
                FROM OrderItems oi
                JOIN Products p ON p.id = oi.product_id
                WHERE oi.order_id = :order_id
            """),
            {"order_id": order["id"]}
        ).mappings()

        order["items"] = [dict(item_row) for item_row in items_result]
        orders.append(order)

    return orders

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

    db.commit()
    return {"message": "Order created successfully", "order_id": order_id}


# Update an existing order
def update_order(db: Session, order_id: int, order_data: OrderUpdate):
    update_fields = []
    update_values = {"id": order_id}

    if order_data.user_id is not None:
        update_fields.append("user_id = :user_id")
        update_values["user_id"] = order_data.user_id

    if order_data.order_date is not None:
        update_fields.append("order_date = :order_date")
        update_values["order_date"] = order_data.order_date

    if order_data.status is not None:
        update_fields.append("status = :status")
        update_values["status"] = order_data.status

    if not update_fields:
        return {"message": "No fields to update."}

    query = f"UPDATE Orders SET {', '.join(update_fields)} WHERE id = :id"
    db.execute(text(query), update_values)
    db.commit()
    return {"message": "Order updated successfully"}

# Delete an order
def delete_order(db: Session, order_id: int):
    db.execute(text("DELETE FROM Orders WHERE id = :id"), {"id": order_id})
    db.commit()
    return {"message": "Order deleted successfully"}
