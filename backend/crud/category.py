from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.category import CategoryCreate, CategoryUpdate

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(text("SELECT * FROM categories")).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, category_id: int):
    result = db.execute(
        text("SELECT * FROM categories WHERE id = :id"),
        {"id": category_id}
    ).first()
    return dict(result) if result else None

def create_category(db: Session, category: CategoryCreate):
    db.execute(
        text("INSERT INTO categories (name) VALUES (:name)"),
        {"name": category.name}
    )
    db.commit()
    return {"message": "Category created successfully"}

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db.execute(
        text("UPDATE categories SET name = :name WHERE id = :id"),
        {"name": category.name, "id": category_id}
    )
    db.commit()
    return {"message": "Category updated successfully"}

def delete_category(db: Session, category_id: int):
    db.execute(
        text("DELETE FROM categories WHERE id = :id"),
        {"id": category_id}
    )
    db.commit()
    return {"message": "Category deleted successfully"}
