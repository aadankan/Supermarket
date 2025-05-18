from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey("Categories.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("Suppliers.id"), nullable=False)
    image_url = Column(String(255))
    