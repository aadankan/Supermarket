from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("SELECT * FROM Products LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).mappings()
    return [dict(row) for row in result]

def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("SELECT * FROM Products WHERE category_id = :category_id LIMIT :limit OFFSET :skip"),
        {"category_id": category_id, "limit": limit, "skip": skip}
    ).mappings()
    return [dict(row) for row in result]

def get_products_with_categories_and_suppliers_and_inventory(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("""
            SELECT 
                p.id AS product_id, p.name AS product_name, p.description AS product_description, p.price AS product_price, p.image_url AS product_image_url, p.category_id as product_category_id,
                s.name AS supplier_name, s.phone_number AS supplier_phone_number,
                i.quantity AS inventory_quantity, i.location AS inventory_location
            FROM Products p
            JOIN Suppliers s ON p.supplier_id = s.id
            JOIN Inventory i ON p.id = i.product_id
            LIMIT :limit OFFSET :skip
        """),
        {"limit": limit, "skip": skip}
    ).mappings()

    return [
        {
            "id": row["product_id"],
            "name": row["product_name"],
            "description": row["product_description"],
            "price": row["product_price"],
            "image_url": row["product_image_url"],
            "category_id": row["product_category_id"],
            "supplier_name": row["supplier_name"],
            "supplier_phone_number": row["supplier_phone_number"],
            "inventory_quantity": row["inventory_quantity"],
            "inventory_location": row["inventory_location"]
        } for row in result
    ]

def get_by_id(db: Session, product_id: int):
    result = db.execute(
        text("SELECT * FROM Products WHERE id = :id"),
        {"id": product_id}
    ).mappings().first()
    return dict(result) if result else None


def create_product(db: Session, product: ProductCreate):
    db.execute(
        text("""
            INSERT INTO Products 
            (name, description, price, count, category_id, supplier_id, image_url) 
            VALUES 
            (:name, :description, :price, :count, :category_id, :supplier_id, :image_url)
        """),
        {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "count": product.count,
            "category_id": product.category_id,
            "supplier_id": product.supplier_id,
            "image_url": product.image_url,
        }
    )
    db.commit()
    return {"message": "Product created successfully"}

def update(db: Session, product_id: int, product_data: ProductUpdate):
    values = product_data.dict(exclude_unset=True)
    if not values:
        return {"message": "No data to update"}
    
    set_clause = ", ".join(f"{key} = :{key}" for key in values.keys())
    values["id"] = product_id

    db.execute(text(f"UPDATE Products SET {set_clause} WHERE id = :id"), values)
    db.commit()
    return {"message": "Product updated successfully"}

def delete(db: Session, product_id: int):
    result = db.execute(text("DELETE FROM Products WHERE id = :id"), {"id": product_id})
    db.commit()
    if result.rowcount:
        return {"message": "Product deleted successfully"}
    else:
        return {"error": "Product not found"}
