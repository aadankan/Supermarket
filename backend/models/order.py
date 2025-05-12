from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    order_date = Column(String(50), nullable=False)  # Use appropriate date type if needed
    shipping_address = Column(String(255), nullable=False)
    billing_address = Column(String(255), nullable=False)
    payment_method = Column(String(50), nullable=False)  # e.g., 'credit_card', 'paypal'
    shipping_method = Column(String(50), nullable=False)  # e.g., 'standard', 'express'
    tracking_number = Column(String(100), nullable=True)
    items = Column(String(255), nullable=False)  # JSON or comma-separated values of item IDs
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)  # e.g., 'pending', 'completed', 'canceled'

