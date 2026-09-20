from fastapi.testclient import TestClient
from src.processing.services import load_regressor
from src.api.main import app
from unittest.mock import patch

client  = TestClient(app)

def test_load_regressor_success():
    """
        Fonction qui teste si le model persisté charge bien
    """

    model = load_regressor()

    assert model is not None
    assert hasattr(model, "predict") #Vérifie que c'est bien un modèle scikit-learn avec l'attribut pour la prédiction



@patch("src.processing.services.joblib.load")
def test_load_regressor_file_not_found(mock_load):
    """
        Vérifie que la fonction gère bien l'absence du fichier modèle.
    """
    #Forcer volontairement joblib.load à déclencher une erreur
    mock_load.side_effect = FileNotFoundError()
    
    model = load_regressor()
    
    assert model is None