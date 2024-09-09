from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

class Equipment(Base):
    __tablename__ = 'Equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    last_updated = Column(DateTime)
    average = Column(Numeric(precision=10, scale=2))