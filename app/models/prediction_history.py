from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base


class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    churn_probability = Column(Float, nullable=False)
    attrition = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    employee_id = Column(Integer, ForeignKey("employee_attrition.id"), nullable=False)

    user = relationship("User", back_populates="history")
