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
from fastapi import APIRouter, Depends
import pandas as pd
import joblib
import json

model = joblib.load("./ml/model_smote.pkl")

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.post("/predict-attrition/")
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
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    prediction = PredictionHistory(
        user_id=current_user.id,
        employee_id=employee_data.id,
        churn_probability=round(float(prob), 4),
        attrition=int(pred),
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
async def predict_attrition(
    request: RetentionPlanRequest, db: Session = Depends(get_db)
):
    prediction = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.id == request.prediction_id)
        .first()
    )
    if not prediction:
        return {"error": "Prediction not found"}
    employee = (
        db.query(EmployeeAttrition)
        .filter(EmployeeAttrition.id == prediction.employee_id)
        .first()
    )

    if prediction.churn_probability < 0.50:
        return {"message": "Low risk detected. No retention plan required."}

    plan_text = gemini_service(employee, prediction, GeminiResponse)
    if isinstance(plan_text, str):
        plan_text = json.loads(plan_text)

    action_one = plan_text["retention_plan"][0]
    action_two = plan_text["retention_plan"][1]
    action_three = plan_text["retention_plan"][2]

    plans = [action_one, action_two, action_three]

    new_plan = RetentionPlan(prediction_id=prediction.id, plan_content=plans)
    db.add(new_plan)
    db.commit()

    return new_plan
