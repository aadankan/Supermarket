from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    order_date = Column(String(50), nullable=False)  # Ideally DateTime
    status = Column(String(50), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("Addresses.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("Addresses.id"), nullable=False)
