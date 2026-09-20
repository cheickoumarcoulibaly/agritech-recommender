from datetime import datetime, timezone

from sqlalchemy import Boolean, Float, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    Region: Mapped[str] = mapped_column(String)
    Soil_Type: Mapped[str] = mapped_column(String)
    Crop: Mapped[str] = mapped_column(String)
    Rainfall_mm: Mapped[float] = mapped_column(Float)
    Temperature_Celsius: Mapped[float] = mapped_column(Float)
    Fertilizer_Used: Mapped[bool] = mapped_column(Boolean)
    Irrigation_Used: Mapped[bool] = mapped_column(Boolean)
    Weather_Condition: Mapped[str] = mapped_column(String)
    Days_to_Harvest: Mapped[int] = mapped_column(Integer)
    pesticides_tonnes_mean: Mapped[float] = mapped_column(Float)

    predicted_yield: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )