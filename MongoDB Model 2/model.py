#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Optional

class FlightPassenger(BaseModel):
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

class Recomendacion(BaseModel):
    airline: str = Field(...)
    nombre_restaurante: str = Field(...)
    tipo_cocina: str = Field(...)
    descripcion: str = Field(...)
    rango_precios: str = Field(...)
    calificacion: float = Field(...)
    opiniones: List[str] = Field(default=[])
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "airline": "Delta Airlines",
                "from_airport": "GDL",
                "to_airport": "PDX",
                "capacidad_avion": 100,
                "connection": True,
                "wait": 0
            }
        }

class AeropuertosMayorEspera(BaseModel):
    airline: str = Field(...)
    from_airport: str = Field(...)
    to_airport: str = Field(...)
    capacidad_avion: int = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "airline": "Delta Airlines",
                "from_airport": "GDL",
                "to_airport": "PDX",
                "capacidad_avion": 100,
                "connection": True,
                "wait": 60
            }
        }