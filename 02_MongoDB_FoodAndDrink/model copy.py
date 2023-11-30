#!/usr/bin/env python3
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional

# Schema completo
class FlightPassenger(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_airport: str = Field(..., alias='from')
    to_airport: str = Field(..., alias='to')
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: Optional[str] = Field(default=None)
    connection: bool = Field(...)
    wait: int = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "Aeromexico",
                "from_airport": "GDL",
                "to_airport": "JFK",
                "day": 16,
                "month": 12,
                "year": 2015,
                "age": 52,
                "gender": "unspecified",
                "reason": "Back Home",
                "stay": "Home",
                "transit": "Car rental",
                "connection": False,
                "wait": 0
            }
        }

# Schema completo update
class FlightPassengerUpdate(BaseModel):
    airline: Optional[str]
    from_airport: Optional[str] = Field(alias='from')
    to: Optional[str] = Field(alias='to')
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
    age: Optional[int]
    gender: Optional[str]
    reason: str = Field(...)
    stay: Optional[int]
    transit: Optional[str] = Field(default=None)
    connection: Optional[bool]
    wait: int = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "airline": "Aeromexico",
                "from_airport": "GDL",
                "to_airport": "JFK",
                "day": 16,
                "month": 12,
                "year": 2015,
                "age": 52,
                "gender": "unspecified",
                "reason": "Back Home",
                "stay": "Home",
                "transit": "Car rental",
                "connection": False,
                "wait": 0
            }
        }

# Schema filtrado por espera
class AeropuertosMayorEspera(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_airport: str = Field(..., alias='from')
    to_airport: str = Field(..., alias='to')
    connection: bool = Field(...)
    wait: int = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "Aeromexico",
                "from_airport": "GDL",
                "to_airport": "JFK",
                "connection": True,
                "wait": 60
            }
        }

# Schema filtrado por espera update
class AeropuertosMayorEsperaUpdate(BaseModel):
    airline: Optional[str]
    from_airport: Optional[str] = Field(alias='from')
    to_airport: Optional[str] = Field(alias='to')
    connection: Optional[bool]
    wait: int = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "airline": "Aeromexico",
                "from_airport": "GDL",
                "to_airport": "JFK",
                "connection": True,
                "wait": 60
            }
        }

# Schema alimentos y bebidas
class RecomendacionAlimentoBebida(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airport: str = Field(...)
    restaurant_name: str = Field(...)
    cuisine_type: str = Field(...)
    price_range: str = Field(...)
    rating: float = Field(...)
    opinions: list = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airport": "JFK",
                "restaurant_name": "Tacos Campeche",
                "cuisine_type": "Mexicana",
                "price_range": "300-600",
                "rating": 4.3,
                "opinions": ["Buenísimo", "Poco caro, pero son rápidos"]
            }
        }

# Schema alimentos y bebidas update
class RecomendacionAlimentoBebidaUpdate(BaseModel):
    airport: Optional[str]
    restaurant_name: Optional[str]
    cuisine_type: Optional[str]
    price_range: Optional[str]
    rating: Optional[float]
    opinions: Optional[list]
    
    class Config:
        schema_extra = {
            "example": {
                "airport": "JFK",
                "restaurant_name": "Tacos Campeche",
                "cuisine_type": "Mexicana",
                "price_range": "300-600",
                "rating": 4.3,
                "opinions": ["Buenísimo", "Poco caro, pero son rápidos"]
            }
        }
