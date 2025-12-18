from ...schemas.user_schema import EmployeeAttritionRequest
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.prediction_history import PredictionHistory
from ...models.employee_attrition import EmployeeAttrition
from ...authentication.auth import get_current_user
from ...schemas.user_schema import UserSchema
from fastapi import APIRouter, Depends
import pandas as pd
import joblib

model = joblib.load("./ml/model_smote.pkl")

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.get("/")
def get_predict():
    return {"predict": "Hello from predict routes"}


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
        "employee_id": employee_data.id,
        "prediction": prediction.attrition,
        "probability": prediction.churn_probability,
    }
