import joblib
import pandas as pd
import os

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
        return regressor
    except FileNotFoundError:
        return None

REGRESSOR = load_regressor()


def make_prediction(data: dict) -> dict:
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
        #Prétraitement
        input_data = pd.DataFrame([data])
        yield_tons_per_hectare_pred = REGRESSOR.predict(input_data)
        yield_tons_per_hectare_pred = float(yield_tons_per_hectare_pred[0])
        return {
            "yield_tons_per_hectare_pred": yield_tons_per_hectare_pred,
            "input": data
        }

    except Exception as e:
        return {
            "error": f"Prediction failed during processing: {str(e)}" 
        }