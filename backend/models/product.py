from sqlalchemy import Column, Integer, String, DECIMAL
from app.database import Base

class Product(Base):
    __tablename__ = "produkty"

    id = Column(Integer, primary_key=True, index=True)
    nazwa = Column(String(150), nullable=False)
    opis = Column(String(255), nullable=True)
    cena = Column(DECIMAL(10, 2), nullable=False)
    ilosc = Column(Integer, default=0)
