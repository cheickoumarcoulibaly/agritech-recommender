import joblib
import pandas as pd
import os
from src.core.logging import logger


# #Configuration globale: format de l'heure, le niveau d'alerte et le message
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__) #logger spécifique au fichier

REGRESSOR_PATH = os.path.join(os.path.dirname(__file__), "../..", "models", "best_xgb_pipeline.pkl")

"""
    Script servant à charger le modèle de régression et de faire une prédiction
"""

def load_regressor():
    """
        Fonction permettant de charger le modèle de régression optimisé

        ----- return
        regressor: un modèle de régression basé sur Xgboost
    """

    try:

        regressor = joblib.load(REGRESSOR_PATH)
        logger.info("Pipeline du modèle chargé avec succès.")

        return regressor
    
    except FileNotFoundError:

        logger.error("❌ Fichier modèle introuvable au chemin : %s", REGRESSOR_PATH)

        return None

REGRESSOR = load_regressor()


def make_prediction(data: dict, recommendation=False) -> dict:
    """
        Fonction permettant de faire une prédiction à partir des données envoyées par l'utilisateur
        
        ------ params
        data: Dict
        les données brutes d'une plantation

        ----- return
        Un dictionnaire avec la prédiction et des métriques
    """

    if REGRESSOR is None:
        return {
            "error": "Regressor is not available check models/best_xgb_pipeline.pkl"
        }

    try:
        #Prétraitements
        input_data = pd.DataFrame(data)
        yield_tons_per_hectare_pred = REGRESSOR.predict(input_data)

        #Pour une prédiction simple
        if not recommendation:

            yield_tons_per_hectare_pred = float(yield_tons_per_hectare_pred[0])
            logger.info("✅ Prédiction calculée avec succès. %s", yield_tons_per_hectare_pred)

            return {
                "yield_tons_per_hectare_pred": yield_tons_per_hectare_pred,
                "input": data
            }

        #Pour une recommendation de culture
        else:

            predicted_data = input_data.copy()
            predicted_data["predicted_yield"] = yield_tons_per_hectare_pred
            logger.info("Recommandation faite avec succès.")
            
            return{
                "recommended_crop_data": predicted_data.iloc[predicted_data["predicted_yield"].idxmax()].to_dict(),
                "predicted_data": predicted_data.to_dict(orient="records"),
            }        

    except Exception as e:
        logger.error("❌ Erreur de prédiction : %s", str(e))
        return {
            "error": f"Prediction failed during processing: {str(e)}" 
        }