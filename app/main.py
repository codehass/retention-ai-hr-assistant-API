import os
from fastapi import FastAPI
from .db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import auth, predict
from .config import settings

app = FastAPI(
    title="HR API",
    description=("This HR API"),
)


origins = [settings.FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(predict.router)


@app.get("/", tags=["Home route"])
def get_home():
    return {"message": "Hello to HR Retention API"}
