#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from bson import ObjectId
from pymongo.collection import ReturnDocument

from model import Recomendacion, AeropuertosMayorEspera, FlightPassenger

router = APIRouter()

# Clase auxiliar para la validación del ID de MongoDB
class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return str(v)


# Ruta para crear el modelo inicial
@router.post("/", response_description="Agregar un nuevo pasajero", response_model=FlightPassenger, status_code=status.HTTP_201_CREATED)
def create_flight_passenger(request: Request, passenger: FlightPassenger = Body(...)):
    passenger = jsonable_encoder(passenger)
    new_passenger = request.app.database["flight_passenger"].insert_one(passenger)
    created_passenger = request.app.database["flight_passenger"].find_one({"_id": new_passenger.inserted_id})
    
    return created_passenger


@router.get("/", response_description="Traer todas las rutas", response_model=List[FlightPassenger])
def list_passengers(request: Request):
    passengers = list(request.app.database["flight_passenger"].find({"airline": {"$gte": airline}}))
    return passengers


@router.get("/recomendaciones/aeropuerto/{aeropuerto}", response_model=List[Recomendacion])
def obtener_recomendaciones_por_aeropuerto(aeropuerto: str):
    recomendaciones = db.query(Recomendacion).filter(Recomendacion.aeropuerto == aeropuerto).all()
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="Recomendaciones no encontradas")
    return recomendaciones


@router.get("/recomendaciones/buscar", response_model=List[Recomendacion])
def buscar_recomendaciones(tipo_cocina: str, calificacion_minima: float):
    recomendaciones = db.query(Recomendacion).filter(
        Recomendacion.tipo_cocina == tipo_cocina,
        Recomendacion.calificacion >= calificacion_minima
    ).all()
    return recomendaciones


@router.put("/recomendaciones/{id_recomendacion}/calificacion", response_model=Recomendacion)
def actualizar_calificacion(id_recomendacion: str, nueva_calificacion: float):
    recomendacion = db.query(Recomendacion).filter(Recomendacion.id == id_recomendacion).first()
    if recomendacion is None:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    recomendacion.calificacion = nueva_calificacion
    db.commit()
    return recomendacion


@router.post("/recomendaciones/{id_recomendacion}/opinion")
def insertar_opinion(id_recomendacion: str, opinion: str, request: Request):
    recomendacion = request.app.database["recomendaciones"].find_one({"_id": id_recomendacion})
    if not recomendacion:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")

    updated_recomendacion = request.app.database["recomendaciones"].find_one_and_update(
        {"_id": id_recomendacion},
        {"$push": {"opiniones": opinion}},
        return_document=ReturnDocument.AFTER
    )

    return updated_recomendacion


@router.delete("/recomendaciones/{id_recomendacion}/opinion/{id_opinion}")
def eliminar_opinion(id_recomendacion: str, id_opinion: str, request: Request):
    recomendacion = request.app.database["recomendaciones"].find_one({"_id": id_recomendacion})
    if not recomendacion:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")

    if id_opinion not in recomendacion["opiniones"]:
        raise HTTPException(status_code=404, detail="Opinión no encontrada")

    updated_recomendacion = request.app.database["recomendaciones"].find_one_and_update(
        {"_id": id_recomendacion},
        {"$pull": {"opiniones": id_opinion}},
        return_document=ReturnDocument.AFTER
    )

    return updated_recomendacion


@router.post("/", response_description="Agregar colección con rutas con mayor espera", response_model=AeropuertosMayorEspera, status_code=status.HTTP_201_CREATED)
def add_filtered_flight_info(request: Request, vuelo_info: AeropuertosMayorEspera = Body(...)):
    if vuelo_info.connection and vuelo_info.wait > 60:
        new_vuelo = jsonable_encoder(vuelo_info)
        inserted_vuelo = request.app.database["AeropuertosMayorEspera"].insert_one(new_vuelo)
        aeropuerto_recomendación = request.app.database["AeropuertosMayorEspera"].find_one({"_id": inserted_vuelo.inserted_id})

        if created_vuelo is None:
            raise HTTPException(status_code=404, detail="Vuelo no pudo ser creado")

        return aeropuerto_recomendación
    else:
        raise HTTPException(status_code=400, detail="Vuelo no cumple con los criterios de conexión y espera")
    