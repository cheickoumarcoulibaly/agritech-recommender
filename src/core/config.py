from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_url: str = "http://127.0.0.1:8000" # Valeur par défaut au cas où
    database_url: str = "sqlite:///./src/data/agritech.db"
    model_path: str = "models/best_xgb_pipeline.pkl"

    class Config:
        env_file = ".env"

#Instancier la classe une seule fois
settings = Settings()