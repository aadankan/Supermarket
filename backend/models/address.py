from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Address(Base):
    __tablename__ = "Addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(Integer, default=0)
    created_at = Column(String(50), nullable=False)

    # Relationship
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="shipping_address", foreign_keys="Order.shipping_address_id")
    billing_orders = relationship("Order", back_populates="billing_address", foreign_keys="Order.billing_address_id")
