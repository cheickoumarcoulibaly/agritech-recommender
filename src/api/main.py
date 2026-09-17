from fastapi import FastAPI, HTTPException
from src.processing.services import make_prediction
from src.processing.schemas import CropData


#Initialisation de l"API
app = FastAPI(
    title="Agritech - Recommender ML-API / Yield per ton prediction",
    description="API fro predicting yield per ton of culture with crop params",
    version="1.0.0"
)

#Endpoint de santé
@app.get("/", tags=["Heath Check"])
def home():
    """
        Endpoint de base poiur vérifier que l'API est en cours d'exécution
    """

    return {
        "status": "ok",
        "message": "Agritech - Recommender ML API running"
    }

@app.post("/predict-yield", tags=["Yield per tonne"])
def predict_yield(data:CropData):
    """
        Endpoint qui prédit le rendemment d'un culture en fonction des paramètres qui lui sont fournis
    """

    #Appel au pipeline chargé
    result = make_prediction(data.model_dump())

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result