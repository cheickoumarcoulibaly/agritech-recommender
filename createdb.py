from src.core.database import Base, engine
from src.models.prediction import Prediction

Base.metadata.create_all(bind=engine)