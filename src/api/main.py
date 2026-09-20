from fastapi import FastAPI, HTTPException
from src.processing.services import make_prediction
from src.processing.schemas import CropData, CropRecommendedData, Crop
from src.core.logging import logger


#Configuration globale: format de l'heure, le niveau d'alerte et le message
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__) #logger spécifique au fichier

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

@app.post("/predict", tags=["Yield per tonne"])
def predict_yield(data:CropData):
    """
        Endpoint qui prédit le rendemment d'un culture en fonction des paramètres qui lui sont fournis
    """

    logger.info("Reçu une demande de prédiction simple pour la culture : %s", data.Crop.value)

    #Appel au pipeline chargé
    result = make_prediction([data.model_dump()])

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.post("/recommend", tags=["Crop Recommendation"])
def recommended_crop(data:CropRecommendedData):
    """
        Endpoint qui prédit la meilleure(recommendation) culture à faire pour un haut rendement en fonction des conditions d'une parcelle
    """

    logger.info("Reçu une demande de recommandation de culture.")

    data_sended = data.model_dump()
    data = []

    #Créer un dictionnaire avec toutes les éventualités
    for crop in Crop:
        data.append({ **data_sended, "Crop": crop.value})


    #Faire appel au pipeline de prédiction
    result = make_prediction(data=data, recommendation=True)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    logger.info("🏆 Culture recommandée : %s", result["recommended_crop_data"]["Crop"])
    return result

    