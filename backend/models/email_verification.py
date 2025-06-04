from sqlalchemy import CHAR, DateTime, ForeignKey, String, Boolean, Column
from sqlalchemy.orm import relationship

from models.database import Base

import uuid
from datetime import datetime

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(255), ForeignKey("Users.email"), unique=True, index=True, nullable=False)  # FK tutaj
    token = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="email_verification", uselist=False)