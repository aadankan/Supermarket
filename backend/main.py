from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.database import Base, engine, SessionLocal
from models import product, category, user, inventory, order, order_item, supplier, transaction, address, email_verification
from routers import product, category, user, inventory, order, order_item, supplier, transaction, address, email_verification, auth

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Supermarket API")

origins = [
    "http://localhost:5173",  # adres frontendu
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # zezwól na zapytania z tego origin
    allow_credentials=True,
    allow_methods=["*"],           # zezwól na wszystkie metody (GET, POST, itd)
    allow_headers=["*"],           # zezwól na wszystkie nagłówki
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}
    

# Routers
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(category.router, prefix="/categories", tags=["categories"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(order.router, prefix="/orders", tags=["orders"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(order_item.router, prefix="/order-items", tags=["order_items"])
app.include_router(supplier.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
app.include_router(address.router, prefix="/addresses", tags=["addresses"])
app.include_router(email_verification.router, prefix="/email-verification", tags=["email_verification"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])