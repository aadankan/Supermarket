from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Inventory(Base):
    __tablename__ = "Inventory"

    product_id = Column(
        Integer,
        ForeignKey("Products.id", ondelete="CASCADE"),
        primary_key=True
    )
    quantity = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)

    product = relationship(
        "Product",
        back_populates="inventory",
        passive_deletes=True  # Pozwala bazie samodzielnie usuwać zależne rekordy
    )
