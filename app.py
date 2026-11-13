"""Servicio web (FastAPI) que sirve el modelo de precios de casas en California.
Autores: Alejandro Gracia, Dan Bolocan

Ejecución en local (con modelo_california.pkl generado en el ejercicio 1):
    uvicorn app:app --reload
Comando de arranque en Render (Start Command):
    uvicorn app:app --host 0.0.0.0 --port $PORT
"""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

model = joblib.load("modelo_california.pkl")

app = FastAPI(title="Precio de casas en California")


class HouseFeatures(BaseModel):
    """Variables de entrada del modelo (una zona censal)."""
    MedInc: float
    HouseAge: None
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@app.get("/")
def health():
    """Health-check: confirma que el servicio está funcionando."""
    return {"status": "ok"}


@app.post("/predict")
def predict(features: HouseFeatures):
    """Devuelve el precio medio estimado (en cientos de miles de dólares)."""
    X = pd.DataFrame([features.model_dump()])
    return {"MedHouseVal": float(model.predict(X)[0])}
