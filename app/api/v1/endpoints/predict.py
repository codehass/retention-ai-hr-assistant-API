import json
import logging
import time
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.employee import EmployeeAttrition
from app.models.prediction import PredictionHistory
from app.models.retention_plan import RetentionPlan
from app.models.user import User
from app.schemas.employee import EmployeeAttritionRequest
from app.schemas.prediction import (
    GeminiResponse,
    PredictionResponse,
    RetentionPlanRequest,
    RetentionPlanResponse,
)
from app.services.gemini import gemini_service
from app.services.ml import ml_service
from app.services.mlflow import mlflow_service

router = APIRouter(prefix="/predict", tags=["Prediction"])

logger = logging.getLogger(__name__)


@router.post("/attrition", response_model=PredictionResponse)
async def predict_attrition(
    employee_data: EmployeeAttritionRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PredictionResponse:
    start_time = time.perf_counter()

    employee = EmployeeAttrition(**employee_data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)

    df = pd.DataFrame([employee_data.model_dump()])
    prediction, probability = ml_service.predict(df)

    prediction_record = PredictionHistory(
        user_id=current_user.id,
        employee_id=employee.id,
        churn_probability=round(float(probability), 4),
        attrition=prediction,
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    latency_ms = (time.perf_counter() - start_time) * 1000

    try:
        mlflow_service.log_prediction(
            user_id=current_user.id,
            prediction_id=prediction_record.id,
            employee_data=employee_data.model_dump(),
            prediction=prediction,
            probability=float(probability),
            latency_ms=latency_ms,
        )
    except Exception as e:
        logger.warning("Failed to log prediction to MLflow: %s", str(e))

    logger.info(
        "Prediction created for employee %s by user %s: probability=%.4f",
        employee.id,
        current_user.id,
        probability,
    )

    return prediction_record


@router.post("/retention-plan", response_model=RetentionPlanResponse)
async def generate_retention_plan(
    request: RetentionPlanRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> RetentionPlan:
    start_time = time.perf_counter()

    prediction = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.id == request.prediction_id)
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found"
        )

    if prediction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this prediction",
        )

    employee = (
        db.query(EmployeeAttrition)
        .filter(EmployeeAttrition.id == prediction.employee_id)
        .first()
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    if prediction.churn_probability < 0.50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Employee attrition risk is too low to generate a retention plan",
        )

    try:
        plan_text = gemini_service(employee, prediction, GeminiResponse)
        plan_data = json.loads(plan_text)
        plans = plan_data.get("retention_plan", [])
    except json.JSONDecodeError:
        logger.warning("Failed to parse Gemini response, using default plan")
        plans = ["Review compensation", "Schedule 1-on-1", "Discuss career path"]
    except Exception as e:
        logger.error("Gemini service error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate retention plan",
        ) from e

    if not plans:
        plans = ["Review compensation", "Schedule 1-on-1", "Discuss career path"]

    retention_plan = RetentionPlan(prediction_id=prediction.id, plan_content=plans)
    db.add(retention_plan)
    db.commit()
    db.refresh(retention_plan)

    latency_ms = (time.perf_counter() - start_time) * 1000

    try:
        mlflow_service.log_retention_plan(
            prediction_id=prediction.id,
            plan_content=plans,
            latency_ms=latency_ms,
        )
    except Exception as e:
        logger.warning("Failed to log retention plan to MLflow: %s", str(e))

    logger.info("Retention plan created for prediction %s", prediction.id)

    return retention_plan


@router.get("/attrition/history", response_model=list[PredictionResponse])
async def get_attrition_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[PredictionHistory]:
    return (
        db.query(PredictionHistory)
        .filter(PredictionHistory.user_id == current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )


@router.get("/retention-plan/history", response_model=list[RetentionPlanResponse])
async def get_retention_plan_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[RetentionPlan]:
    return (
        db.query(RetentionPlan)
        .join(PredictionHistory)
        .filter(PredictionHistory.user_id == current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )
