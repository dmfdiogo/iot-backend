from app.database.pgsql_database import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    last_updated = Column(DateTime)
    average = Column(Numeric(precision=10, scale=2))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'average': self.average
        }