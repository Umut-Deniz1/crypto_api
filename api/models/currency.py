import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from api.db.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String, nullable=False)
    date_ = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    price = Column(Float, nullable=False)
