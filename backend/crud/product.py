from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM Products")).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, product_id: int):
    result = db.execute(text("SELECT * FROM Products WHERE id = :id"), {"id": product_id}).first()
    return dict(result) if result else None

def create_product(db: Session, product: ProductCreate):
    db.execute(text(
        "INSERT INTO Products (name, description, price, count) VALUES (:name, :description, :price, :count)",
        {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "count": product.count
        }
    ))
    db.commit()
    return {"message": "Product created successfully"}

def update(db: Session, product_id: int, product_data: ProductUpdate):
    db.execute(text(
        "UPDATE Products SET name = :name, description = :description, price = :price, count = :count WHERE id = :id",
        {
            "name": product_data.name,
            "description": product_data.description,
            "price": product_data.price,
            "count": product_data.count,
            "id": product_id
        }
    ))
    db.commit()

def delete(db: Session, product_id: int):
    db.execute(text("DELETE FROM Products WHERE id = :id"), {"id": product_id})
    db.commit()
    return True
