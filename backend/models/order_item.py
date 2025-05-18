from sqlalchemy import Column, Integer, ForeignKey, Numeric, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .database import Base

class OrderItems(Base):
    __tablename__ = "OrderItems"

    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # Price per item

    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'product_id'),
    )

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
