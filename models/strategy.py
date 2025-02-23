from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Strategy(Base):
  __tablename__ = "strategies"

  id = Column(Integer, primary_key=True, autoincrement=True)
  symbol = Column(String, nullable=False)
  min_value = Column(Float, nullable=False)
  max_value = Column(Float, nullable=False)
  amount = Column(Float, nullable=False)
  strategy_type = Column(String, default="FIVE_TEN_FIFTEEN")
  active = Column(String, default=False)