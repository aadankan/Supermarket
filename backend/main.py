# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from crud import product as crud_product  # CRUD operations
from schemas.product import Product, ProductCreate  # Pydantic models
from models.database import SessionLocal, engine  # Database session and engine
from models.product import Product as SQLAlchemyProduct  # SQLAlchemy model

# Create tables if they don't exist
SQLAlchemyProduct.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/products", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud_product.get_products(db=db, skip=skip, limit=limit)
    return products

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)
