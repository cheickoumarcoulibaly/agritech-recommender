from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_home():
    """
        Fonction qui teste la route d'accueil de l'API.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict():
    """
        Fonction qui teste la prédiction du rendement
    """

    test_data = {
        "Region": "South",
        "Soil_Type": "Clay",
        "Crop": "Rice",
        "Rainfall_mm": 992.673282,
        "Temperature_Celsius": 18.026142,
        "Fertilizer_Used": True,
        "Irrigation_Used": True,
        "Weather_Condition": "Rainy",
        "Days_to_Harvest": 140,
        "pesticides_tonnes_mean": 36942.215995,
    }

    response = client.post("/predict", json=test_data)
    data = response.json()
    
    assert response.status_code == 200
    assert "yield_tons_per_hectare_pred" in data
    assert "input" in data


def test_bad_predict():
    """
        Fonction qui teste une mauvaise prédiction
    """

    test_data = {
        "Region": "Unknow",
        "Soil_Type": "Clay",
        "Crop": "Rice",
        # "Rainfall_mm": 992.673282,
        "Temperature_Celsius": 18.026142,
        "Fertilizer_Used": True,
        "Irrigation_Used": True,
        "Weather_Condition": "Rainy",
        "Days_to_Harvest": 140,
        "pesticides_tonnes_mean": 36942.215995,
    }

    response = client.post("/predict", json=test_data)

    assert response.status_code == 422


def test_recommend():
    """
        Fonction qui teste une recommendation de culture
    """
    
    test_data = {
        "Region": "West",
        "Soil_Type": "Sandy",
        "Rainfall_mm": 897.077239,
        "Temperature_Celsius": 27.676966,
        "Fertilizer_Used": False,
        "Irrigation_Used": True,
        "Weather_Condition": "Cloudy",
        "Days_to_Harvest": 122,
        "pesticides_tonnes_mean": 0
    }

    response = client.post("/recommend", json=test_data)

    assert response.status_code == 200
    assert "recommended_crop_data" in response.json()
    assert "predicted_data" in response.json()


def test_bad_recommend():

    """
        Fonction qui teste une recommendation de culture
    """

    test_data = {
        "Region": "West",
        "Soil_Type": "Unknow",
        "Rainfall_mm": 897.077239,
        "Temperature_Celsius": 27.676966,
        "Fertilizer_Used": False,
        "Irrigation_Used": True,
        "Weather_Condition": "Cloudy",
        # "Days_to_Harvest": 122,
        "pesticides_tonnes_mean": 0
    }

    response = client.post("/recommend", json=test_data)

    assert response.status_code == 422
