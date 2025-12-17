from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from ..db.database import Base


class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    churn_probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="history")
