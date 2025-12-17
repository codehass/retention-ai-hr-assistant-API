from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.get("/")
def get_predict():
    return {"predict": "Hello from predict routes"}
