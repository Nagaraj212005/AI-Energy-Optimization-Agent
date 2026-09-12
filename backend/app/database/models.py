from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime

from backend.app.database.database import Base

class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)

    datetime = Column(DateTime)

    consumption = Column(Float)

    region = Column(String)

    year = Column(Integer)

    month = Column(Integer)

    day = Column(Integer)

    hour = Column(Integer)

    weekday = Column(String)

    weekend = Column(Boolean)

    peak_hour = Column(Boolean)