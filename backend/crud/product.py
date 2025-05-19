from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("SELECT * FROM Products LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, product_id: int):
    result = db.execute(
        text("SELECT * FROM Products WHERE id = :id"),
        {"id": product_id}
    ).first()
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
