from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class RetentionPlan(Base):
    __tablename__ = "retention_plans"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(
        Integer, ForeignKey("predictions_history.id"), nullable=False, unique=True
    )
    plan_content = Column(JSON, nullable=False)

    prediction = relationship("PredictionHistory", back_populates="retention_plan")
