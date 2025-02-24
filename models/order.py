from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    order_id = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    order_type = Column(String, nullable=False)  # BUY or SELL
    status = Column(String, default="OPEN")  # OPEN, FILLED, CANCELED
