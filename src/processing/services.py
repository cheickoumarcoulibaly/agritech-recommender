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
        #Prétraitement
        input_data = pd.DataFrame(data)
        yield_tons_per_hectare_pred = REGRESSOR.predict(input_data)

        #Pour une prédiction simple
        if not recommendation:

            yield_tons_per_hectare_pred = float(yield_tons_per_hectare_pred[0])
            return {
                "yield_tons_per_hectare_pred": yield_tons_per_hectare_pred,
                "input": data
            }

        #Pour une recommendation de culture
        else:

            predicted_data = input_data.copy()
            predicted_data["predicted_yield"] = yield_tons_per_hectare_pred
            
            return{
                "recommended_crop_data": predicted_data.iloc[predicted_data["predicted_yield"].idxmax()].to_dict(),
                "predicted_data": predicted_data.to_dict(orient="records"),
            }        

    except Exception as e:
        return {
            "error": f"Prediction failed during processing: {str(e)}" 
        }