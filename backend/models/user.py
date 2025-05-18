from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Integer, default=0)
    phone_number = Column(String(15), unique=True, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    default_address_id = Column(Integer, ForeignKey("Addresses.id"), nullable=True)
    created_at = Column(String(50), nullable=False)

    # Relationships
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    default_address = relationship("Address", foreign_keys=[default_address_id], uselist=False, post_update=True)
