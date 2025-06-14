from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    priority_score = Column(Integer)
    status = Column(String, default="Needs Dispatch")
    # Store the complex extracted data as a JSON object
    details = Column(JSON)