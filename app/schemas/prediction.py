from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction_id: int
    employee_id: int
    prediction: int
    probability: float


class RetentionPlanRequest(BaseModel):
    prediction_id: int


class RetentionPlanResponse(BaseModel):
    id: int
    prediction_id: int
    plan_content: list[str]

    model_config = {"from_attributes": True}


class GeminiResponse(BaseModel):
    retention_plan: list[str] = Field(..., min_length=3, max_length=3)
