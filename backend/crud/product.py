from sqlalchemy import text
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(Product).offset(0).limit(100).all()
    result = db.execute(text("SELECT * FROM products")).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, product_id: int):
    # return db.query(Product).filter(Product.id == product_id).first()
    result = db.execute(text("SELECT * FROM products WHERE id = :id"), {"id": product_id}).first()
    return dict(result) if result else None

def create_product(db: Session, product: ProductCreate):
    # db_product = Product(**product.dict())
    # db.add(db_product)
    # db.commit()
    # db.refresh(db_product)
    # return db_product
    db.execute(text(
        "INSERT INTO products (name, description, price, count) VALUES (:name, :description, :price, :count)",
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
    # product = db.query(Product).filter(Product.id == product_id).first()
    # if product:
    #     for key, value in product_data.dict().items():
    #         setattr(product, key, value)
    #     db.commit()
    #     db.refresh(product)
    # return product
    db.execute(text(
        "UPDATE products SET name = :name, description = :description, price = :price, count = :count WHERE id = :id",
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
    # product = db.query(Product).filter(Product.id == product_id).first()
    # if product:
    #     db.delete(product)
    #     db.commit()
    # return product
    db.execute(text("DELETE FROM products WHERE id = :id"), {"id": product_id})
    db.commit()
    return True
