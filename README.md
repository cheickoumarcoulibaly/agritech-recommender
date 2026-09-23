# 🌾 Agritech Answers : Assistant Agricole Intelligent (MLOps)

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27.0-FF4B4B.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Optimized-orange.svg)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue)

**Agritech Answers** est une application d'intelligence artificielle conçue pour le domaine agricole. À partir des conditions environnementales d'une parcelle (météo, type de sol, région, etc.), l'application permet de prédire avec précision le rendement agricole et de recommander la culture la plus rentable.

Ce projet a été développé dans le cadre d'une architecture **MLOps** complète, intégrant l'entraînement de modèles, le suivi des expérimentations, le déploiement via API, une interface utilisateur, et l'intégration continue.

---

## ✨ Fonctionnalités Principales

*   **🧪 Modélisation ML Optimisée :** Utilisation de l'algorithme `XGBoost` avec recherche d'hyperparamètres (RandomizedSearchCV). Score R² en test : > 91%.
*   **📊 Tracking MLflow :** Traçabilité totale des expérimentations, des hyperparamètres et des métriques de performance.
*   **🚀 API REST (FastAPI) :** Service backend ultra-rapide avec validation forte des données via `Pydantic` (Enums).
*   **🖥️ Interface Utilisateur (Streamlit) :** Frontend intuitif pour les agriculteurs permettant des prédictions simples et des recommandations multicritères (Batch Prediction).
*   **💾 Monitoring (SQLite) :** Journalisation de toutes les requêtes entrantes pour une future analyse de *Data Drift*.
*   **🔄 Intégration Continue (CI) :** Workflow GitHub Actions vérifiant automatiquement l'intégrité du code (Pytest) et la compilation de l'image Docker à chaque Pull Request.

---

## 🏗️ Architecture du Projet

```text
Agritech-Recommender/
├── data/                        # Données brutes et nettoyées
├── logs/                        # Logs d'exécution de l'application
├── models/                      # Modèles sérialisés (ex: best_xgb_pipeline.pkl)
├── notebooks/                   # Notebooks Jupyter (EDA, PCA, Entraînement)
├── src/                         # Code source de l'application
│   ├── api/                     # Routeur HTTP (main.py)
│   ├── core/                    # Configurations (Database, Logging, Paramètres)
│   ├── data/                    # Base de données SQLite de production
│   ├── front/                   # Application web Streamlit (app.py)
│   ├── models/                  # Modèles SQLAlchemy (Persistance)
│   └── processing/              # Logique ML et Schémas Pydantic
├── tests/                       # Tests unitaires Pytest avec Mocking
├── .github/workflows/           # Configuration CI/CD (GitHub Actions)
├── Dockerfile                   # Configuration de conteneurisation
└── requirements.txt             # Dépendances Python
```

---

## 🚀 Installation et Démarrage

### 1. Prérequis
*   Python 3.10 ou supérieur (recommandé : 3.14)
*   Git

### 2. Cloner le dépôt et installer les dépendances
```bash
git clone https://github.com/cheickoumarcoulibaly/agritech-recommender
cd agritech-recommender

# Création de l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Mac/Linux
# .venv\Scripts\activate   # Sur Windows

# Installation
pip install -r requirements.txt
```

### 3. Configuration des Variables d'Environnement
Créez un fichier `.env` à la racine du projet pour centraliser vos paramètres :
```env
API_URL=http://127.0.0.1:8000
DATABASE_URL=sqlite:///./src/data/agritech.db
MODEL_PATH=models/best_xgb_pipeline.pkl
```

---

## 🎮 Exécution en local

L'application est divisée en deux services distincts (Backend et Frontend). Il est recommandé d'utiliser deux terminaux.

**Terminal 1 : Lancer l'API FastAPI**
```bash
uvicorn src.api.main:app --reload
```
L'API est désormais disponible sur `http://127.0.0.1:8000`. 
👉 *La documentation interactive (Swagger UI) est consultable sur `http://127.0.0.1:8000/docs`*

**Terminal 2 : Lancer l'interface Streamlit**
```bash
PYTHONPATH=. streamlit run src/front/app.py
```
L'interface graphique s'ouvrira automatiquement dans votre navigateur.

---

## 📡 Endpoints de l'API

*   `GET /` : Health check de l'API.
*   `POST /predict` : Prédit le rendement pour une culture spécifique en fonction des paramètres environnementaux.
*   `POST /recommend` : Simule l'ensemble des cultures possibles et retourne un classement trié de la plus rentable à la moins rentable.

---

## 🛠️ Tests (CI)

Le projet utilise **Pytest** pour garantir la stabilité de l'API. La suite inclut des tests de validation Pydantic (codes 422), des tests nominaux (codes 200), et des tests unitaires avancés utilisant le *Mocking* pour tester la résilience au chargement du modèle.

Pour lancer les tests localement :
```bash
python -m pytest -v
```

---
*Projet réalisé dans le cadre de la formation OpenClassrooms.*
