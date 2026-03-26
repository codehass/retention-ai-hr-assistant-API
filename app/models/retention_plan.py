from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class RetentionPlan(Base):
    __tablename__ = "retention_plans"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(
        Integer, ForeignKey("predictions_history.id"), nullable=False, unique=True
    )
    plan_content = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    prediction = relationship("PredictionHistory", back_populates="retention_plan")
