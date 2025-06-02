from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # precyzyjny typ dla ceny
    description = Column(Text, nullable=True)  # pozwala na dłuższe opisy
    category_id = Column(Integer, ForeignKey("Categories.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("Suppliers.id"), nullable=False)
    image_url = Column(String(255), nullable=True)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    inventory = relationship("Inventory",back_populates="product",cascade="all, delete-orphan")
    order_items = relationship("OrderItems", back_populates="product")
    transactions = relationship("Transaction", back_populates="product")
