from ...schemas.user_schema import EmployeeAttritionRequest
from fastapi import APIRouter
import pandas as pd
import joblib

model = joblib.load("./ml/model_smote.pkl")

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.get("/")
def get_predict():
    return {"predict": "Hello from predict routes"}


@router.post("/predict-attrition/")
async def predict_attrition(employee: EmployeeAttritionRequest):

    df = pd.DataFrame([employee.dict()])

    pred = model.predict(df)
    prob = model.predict_proba(df)[0][1]

    return {"prediction": int(pred), "probability": round(float(prob), 4)}
