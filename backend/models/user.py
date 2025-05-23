from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.database import Base

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    is_admin = Column(Integer, default=0)
    phone_number = Column(String(15), unique=True, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    default_address_id = Column(Integer, ForeignKey("Addresses.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    email_confirmed = Column(Boolean, default=False)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan", foreign_keys="[Address.user_id]")

    default_address = relationship("Address",foreign_keys=[default_address_id],uselist=False,post_update=True)
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    email_verification = relationship("EmailVerification", back_populates="user", uselist=False)
