from sqlalchemy import Column, Integer, String
from .database import Base

class Supplier(Base):
    __tablename__ = "Suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=True)
    contact_number = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)