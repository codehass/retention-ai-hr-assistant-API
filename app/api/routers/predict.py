from ...schemas.user_schema import EmployeeAttritionRequest
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.prediction_history import PredictionHistory
from ...models.employee_attrition import EmployeeAttrition
from ...models.retention_plan import RetentionPlan
from ...authentication.auth import get_current_user
from ...schemas.user_schema import (
    UserSchema,
    RetentionPlanRequest,
    GeminiResponse,
    RetentionPlanResponse,
)
from ...services.service_gemini import gemini_service
from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
import joblib
import json
import logging

model = joblib.load("./ml/model_smote.pkl")

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.post("/predict-attrition")
async def predict_attrition(
    employee: EmployeeAttritionRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    employee_data = EmployeeAttrition(**employee.model_dump())
    db.add(employee_data)
    db.commit()
    db.refresh(employee_data)

    df = pd.DataFrame([employee.model_dump()])
    prob = model.predict_proba(df)[0][1]
    attrition = 1 if prob >= 0.5 else 0

    prediction = PredictionHistory(
        user_id=current_user.id,
        employee_id=employee_data.id,
        churn_probability=round(float(prob), 4),
        attrition=int(attrition),
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "prediction_id": prediction.id,
        "employee_id": employee_data.id,
        "prediction": prediction.attrition,
        "probability": prediction.churn_probability,
    }


@router.post("/generate-retention-plan", response_model=RetentionPlanResponse)
async def generate_retention_plan_endpoint(
    request: RetentionPlanRequest, db: Session = Depends(get_db)
):
    try:
        prediction = (
            db.query(PredictionHistory)
            .filter(PredictionHistory.id == request.prediction_id)
            .first()
        )
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")

        employee = (
            db.query(EmployeeAttrition)
            .filter(EmployeeAttrition.id == prediction.employee_id)
            .first()
        )
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        if prediction.churn_probability < 0.50:
            raise HTTPException(
                status_code=422,
                detail="Employee attrition risk is too low to generate a retention plan.",
            )

        plan_text = gemini_service(employee, prediction, GeminiResponse)

        if isinstance(plan_text, str):
            try:
                plan_text = json.loads(plan_text)
            except json.JSONDecodeError:
                logging.warning("Failed to parse Gemini response. Using default plan.")
                plan_text = {}

        plans = plan_text.get("retention_plan", [])

        if not plans:
            logging.info("Using default retention plan for employee ID %s", employee.id)
            plans = ["Review compensation", "Schedule 1-on-1", "Discuss career path"]

        new_plan = RetentionPlan(prediction_id=prediction.id, plan_content=plans)
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        return new_plan

    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error generating retention plan: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")
