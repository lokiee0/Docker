from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.train import MODEL_PATH

model = None


class Flower(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError("Model missing. Run: python -m src.train")
    model = joblib.load(MODEL_PATH)
    yield
    model = None


app = FastAPI(title="Iris model API", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(flower: Flower) -> dict:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    values = [[flower.sepal_length, flower.sepal_width, flower.petal_length, flower.petal_width]]
    return {"predicted_class": int(model.predict(values)[0])}
