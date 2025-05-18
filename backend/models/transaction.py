from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from .database import Base

class Transaction(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    change = Column(Integer, nullable=False)  # Positive for addition, negative for removal
    transaction_type = Column(String(50), nullable=False)  # e.g., 'purchase', 'return', 'restock'
    timestamp = Column(DateTime, nullable=False)
    note = Column(String(255), nullable=True)  # Optional note about the transaction
    