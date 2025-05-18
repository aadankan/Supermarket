from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Transaction(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    quantity_change = Column(Integer, nullable=False)  # Positive for addition, negative for removal
    transaction_type = Column(String(50), nullable=False)  # e.g., 'purchase', 'return', 'restock'
    timestamp = Column(DateTime, nullable=False)
    note = Column(Text, nullable=True)  # Optional note about the transaction

    product = relationship("Product", back_populates="transactions")    