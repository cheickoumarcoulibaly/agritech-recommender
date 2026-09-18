from pydantic import BaseModel
from enum import Enum

"""
    Script servant à la création du format attendu par l'API
"""

class Region(str, Enum):
    WEST = "West"
    SOUTH = "South"
    NORTH = "North"
    EAST = "East"

class SoilType(str, Enum):
    SANDY = "Sandy"
    CLAY = "Clay"
    LOAM = "Loam"
    SILT = "Silt"
    PEATY = "Peaty"
    CHALKY = "Chalky"

class Crop(str, Enum):
    COTTON = "Cotton"
    RICE = "Rice"
    BARLEY = "Barley"
    SOYBEAN = "Soybean"
    WHEAT = "Wheat"
    MAIZE = "Maize"

class WeatherCondition(str, Enum):
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    SUNNY = "Sunny"

class CropData(BaseModel):
    Region: Region
    Soil_Type: SoilType
    Crop: Crop
    Rainfall_mm: float
    Temperature_Celsius: float
    Fertilizer_Used: bool
    Irrigation_Used: bool
    Weather_Condition: WeatherCondition
    Days_to_Harvest: int
    pesticides_tonnes_mean: float

class CropRecommendedData(BaseModel):
    Region: Region
    Soil_Type: SoilType
    Rainfall_mm: float
    Temperature_Celsius: float
    Fertilizer_Used: bool
    Irrigation_Used: bool
    Weather_Condition: WeatherCondition
    Days_to_Harvest: int
    pesticides_tonnes_mean: float