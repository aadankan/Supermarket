from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.category import CategoryCreate, CategoryUpdate

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(
        text("SELECT * FROM Categories ORDER BY id LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, category_id: int):
    result = db.execute(
        text("SELECT * FROM Categories WHERE id = :id"),
        {"id": category_id}
    ).mappings().first()  # Use .mappings() to get dict-like rows
    return dict(result) if result else None

def create_category(db: Session, category: CategoryCreate):
    # Możesz tu dodać obsługę unikalności, jeśli baza zwraca błąd to wyłap w routerze
    db.execute(
        text("INSERT INTO Categories (name) VALUES (:name)"),
        {"name": category.name}
    )
    db.commit()
    # Po utworzeniu możesz pobrać i zwrócić nowo dodaną kategorię
    result = db.execute(
        text("SELECT * FROM Categories WHERE name = :name"),
        {"name": category.name}
    ).first()
    return dict(result) if result else {"message": "Category created successfully"}

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db.execute(
        text("UPDATE Categories SET name = :name WHERE id = :id"),
        {"name": category.name, "id": category_id}
    )
    db.commit()
    # Pobierz zaktualizowany rekord
    result = db.execute(
        text("SELECT * FROM Categories WHERE id = :id"),
        {"id": category_id}
    ).mappings().first()
    return dict(result) if result else {"message": "Category updated successfully"}

def delete_category(db: Session, category_id: int):
    db.execute(
        text("DELETE FROM Categories WHERE id = :id"),
        {"id": category_id}
    )
    db.commit()
    return {"message": "Category deleted successfully"}
