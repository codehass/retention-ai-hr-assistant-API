from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    employee_id = Column(
        Integer, ForeignKey("employee_attrition.id"), nullable=False, index=True
    )
    churn_probability = Column(Float, nullable=False)
    attrition = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="predictions")
    employee = relationship("EmployeeAttrition", back_populates="predictions")
    retention_plan = relationship(
        "RetentionPlan", back_populates="prediction", uselist=False
    )
