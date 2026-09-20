from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'agritech.db'}"


#Créer le moteur de base
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#Créer une session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Créer la base
Base = declarative_base()


def get_db():
    """Fonction qui permet de générer une session de communication avec la base de données"""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
