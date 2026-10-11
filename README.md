# 🌾 Agritech Answers

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

**Agritech Answers** estime le rendement d’une culture à partir des conditions d’une parcelle et compare plusieurs cultures pour proposer une recommandation. Le projet réunit un modèle XGBoost, une API FastAPI et une interface Streamlit.

## 🌱 Le parcours d’une prédiction

```text
Conditions de la parcelle → API FastAPI → Pipeline XGBoost → Rendement estimé
                                      └→ SQLite : historique de /predict
```

- `POST /predict` estime le rendement de la culture choisie.
- `POST /recommend` compare les six cultures disponibles et renvoie le meilleur rendement prédit.
- L’interface Streamlit permet de saisir les conditions et de consulter les résultats.

## 🚀 Démarrage rapide avec Docker

Depuis la racine du dépôt, crée un fichier `.env` :

```env
API_URL=http://127.0.0.1:8000
DATABASE_URL=sqlite:///./src/data/agritech.db
MODEL_PATH=models/best_xgb_pipeline.pkl
```

Puis construis l’image et lance l’API :

```bash
docker build -t agritech-api .
docker run --env-file .env -p 8000:8000 --name agritech-api agritech-api:latest
```

L’API et sa documentation sont disponibles à <http://127.0.0.1:8000> et <http://127.0.0.1:8000/docs>.

> Le conteneur Docker lance l’API uniquement. Sans volume Docker, l’historique SQLite est supprimé avec le conteneur.

## 💻 Lancer en local

### Installer le projet

```bash
git clone https://github.com/cheickoumarcoulibaly/agritech-recommender.git
cd agritech-recommender
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

L’interface nécessite aussi Streamlit et Requests :

```bash
pip install streamlit requests
```

Vérifie que `models/best_xgb_pipeline.pkl` est présent, puis initialise la base locale :

```bash
python createdb.py
```

### Démarrer l’API et l’interface

Dans un premier terminal :

```bash
uvicorn src.api.main:app --reload
```

Dans un second terminal, depuis la racine du projet :

```bash
PYTHONPATH=. streamlit run src/front/app.py
```

Streamlit utilise l’adresse définie dans `API_URL` du fichier `.env`.

## 🔌 Tester les routes

### Vérifier l’API

```bash
curl http://127.0.0.1:8000/
```

### Prédire le rendement (`POST /predict`)

Cette route attend les conditions de la parcelle et le champ `Crop` :

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "Region": "South", "Soil_Type": "Clay", "Crop": "Rice",
    "Rainfall_mm": 992.67, "Temperature_Celsius": 18.03,
    "Fertilizer_Used": true, "Irrigation_Used": true,
    "Weather_Condition": "Rainy", "Days_to_Harvest": 140,
    "pesticides_tonnes_mean": 36942.22
  }'
```

La réponse contient le rendement estimé en tonnes par hectare. Les requêtes de cette route sont enregistrées dans SQLite.

### Comparer les cultures (`POST /recommend`)

Envoie les mêmes conditions, **sans `Crop`**. L’API renvoie les prédictions pour Cotton, Rice, Barley, Soybean, Wheat et Maize, puis la culture avec le rendement estimé le plus élevé.

Les valeurs des catégories doivent respecter les choix définis par l’API. Une entrée invalide renvoie une erreur HTTP 422.

## 📊 Données et modèle

Les sources sont dans `data/raw/` et les fichiers consolidés dans `data/processed/`. Le notebook de fusion et d’ACP produit `dataset_ml_ready.csv`, utilisé par le notebook d’entraînement.

| Notebook | Contenu |
|---|---|
| `01_exploration.ipynb` | Exploration des sources |
| `02_exploration-fusion_acp_guide.ipynb` | Fusion, analyses et ACP détaillée |
| `03_model_training.ipynb` | Comparaison et optimisation des modèles |

Le pipeline XGBoost sérialisé se trouve dans `models/best_xgb_pipeline.pkl`. Dans l’expérimentation du notebook, il obtient environ **0,500 t/ha de RMSE** et **0,913 de R²** sur le jeu de test.

⚠️ `pesticides_tonnes_mean` est une moyenne historique agrégée par culture. Les zéros peuvent représenter une correspondance historique absente, et pas nécessairement une absence d’usage de pesticides.

## 🧪 Tests et suivi MLflow

Lancer les tests depuis la racine :

```bash
python -m pytest -v
```

GitHub Actions exécute les tests et construit l’image Docker lors des pull requests vers `main`.

Le notebook d’entraînement utilise MLflow à `http://127.0.0.1:5000`. Dans un autre terminal, tu lances l’interface et le serveur de suivi avec :

```bash
mlflow ui --host 127.0.0.1 --port 5000
```

Le notebook peut aussi pointer directement vers `sqlite:///../mlflow.db` depuis `notebooks/`. [Documentation MLflow](https://mlflow.org/docs/latest/tracking/server/).

## 🧭 Structure

```text
src/api/          Routes FastAPI
src/front/        Interface Streamlit
src/processing/   Schémas et logique de prédiction
src/core/         Configuration, base SQLite et logs
models/           Pipeline entraîné
notebooks/        Exploration, ACP et entraînement
data/             Sources et données préparées
tests/            Tests automatisés
Dockerfile        Image de l’API
```

---

Projet réalisé dans le cadre de la formation OpenClassrooms pas **Coulibaly Cheick Oumar**.
