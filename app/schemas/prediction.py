from datetime import datetime

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction_id: int = Field(alias="id")
    employee_id: int
    prediction: int = Field(alias="attrition")
    probability: float = Field(alias="churn_probability")
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class RetentionPlanRequest(BaseModel):
    prediction_id: int


class RetentionPlanResponse(BaseModel):
    id: int
    prediction_id: int
    plan_content: list[str]
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class GeminiResponse(BaseModel):
    retention_plan: list[str] = Field(..., min_length=3, max_length=3)
