from sqlalchemy import Column, Integer, Text, ForeignKey, JSON
from ..db.database import Base
from sqlalchemy.dialects.postgresql import ARRAY


class RetentionPlan(Base):
    __tablename__ = "retention_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_content = Column(JSON)
    prediction_id = Column(
        Integer, ForeignKey("predictions_history.id"), nullable=False
    )
