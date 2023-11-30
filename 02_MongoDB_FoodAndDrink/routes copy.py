#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
from pymongo.collection import ReturnDocument

from model import FlightPassenger, FlightPassengerUpdate, AeropuertosMayorEspera, AeropuertosMayorEsperaUpdate, RecomendacionAlimentoBebida, RecomendacionAlimentoBebidaUpdate

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


# Ruta para crear el modelo completo
@router.post("/FlightPassenger", response_description="Agregar una nueva ruta", status_code=status.HTTP_201_CREATED, response_model=FlightPassenger)
def create_flight_passenger(request: Request, passenger: FlightPassenger = Body(...)):
    passenger = jsonable_encoder(passenger)
    new_passenger = request.app.database["Flight Routes"].insert_one(passenger)
    created_passenger = request.app.database["Flight Routes"].find_one(
        {"_id": new_passenger.inserted_id}
    )
    return created_passenger

# Ruta para consultar todas las rutas del modelo completo filtrando la espera
@router.get("/FlightPassenger", response_description="Consultar todas las rutas", response_model=List[FlightPassenger])
def list_all_routes(request: Request, wait: int = 0):
    rutas = list(request.app.database["Flight Routes"].find({"wait": {"$gte": wait}}))
    return rutas

# Ruta para actualizar una ruta del modelo completo
@router.put("/FlightPassenger/{id}", response_description="Actualizar ruta por ID de la base de datos completa", response_model=FlightPassenger)
def update_route(id: str, request: Request, route: FlightPassengerUpdate = Body(...)):
    updated_route = request.app.database["Flight Routes"].find_one_and_update(
        {"_id": id},
        {"$set": route.dict(exclude_unset=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_route is not None:
        return updated_route

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")

# Ruta para eliminar una ruta del modelo completo
@router.delete("/FlightPassenger/{id}", response_description="Borrar una ruta por ID de la base de datos completa")
def delete_route(id: str, request: Request, response: Response):
    deleted_route = request.app.database["Flight Routes"].find_one_and_delete({"_id": id})

    if deleted_route is not None:
        return {"message": f"Ruta con ID {id} eliminada correctamente"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")



# Ruta para crear el modelo filtrado
@router.post("/AeropuertosMayorEspera", response_description="Agregar una nueva ruta filtrada", status_code=status.HTTP_201_CREATED, response_model=AeropuertosMayorEspera)
def create_filtered_route(request: Request, passenger: AeropuertosMayorEspera = Body(...)):
    passenger = jsonable_encoder(passenger)
    new_passenger = request.app.database["Rutas Recomendadas"].insert_one(passenger)
    created_passenger = request.app.database["Rutas Recomendadas"].find_one(
        {"_id": new_passenger.inserted_id}
    )
    return created_passenger

# Ruta para consultar todas las rutas filtradas, filtrando la espera
@router.get("/AeropuertosMayorEspera", response_description="Consultar todas las rutas filtradas", response_model=List[AeropuertosMayorEspera])
def list_filtered_routes(request: Request, wait: int = 0):
    rutas = list(request.app.database["Rutas Recomendadas"].find({"wait": {"$gte": wait}}))
    return rutas

# Ruta para actualizar una ruta del modelo filtrado
@router.put("/AeropuertosMayorEspera/{id}", response_description="Actualizar ruta filtrada por ID", response_model=AeropuertosMayorEspera)
def update_filtered_route(id: str, request: Request, route: AeropuertosMayorEsperaUpdate = Body(...)):
    updated_route = request.app.database["Rutas Recomendadas"].find_one_and_update(
        {"_id": id},
        {"$set": route.dict(exclude_unset=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_route is not None:
        return updated_route

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")

# Ruta para eliminar una ruta del modelo filtrado
@router.delete("/AeropuertosMayorEspera/{id}", response_description="Borrar una ruta por ID de la base de datos filtrada")
def delete_filtered_route(id: str, request: Request, response: Response):
    deleted_route = request.app.database["Rutas Recomendadas"].find_one_and_delete({"_id": id})

    if deleted_route is not None:
        return {"message": f"Ruta con ID {id} eliminada correctamente"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")



# Ruta para crear el modelo de restaurantes
@router.post("/RecomendacionAlimentoBebida", response_description="Agregar un nuevo restaurante", status_code=status.HTTP_201_CREATED, response_model=RecomendacionAlimentoBebida)
def create_restaurant(request: Request, restaurant: RecomendacionAlimentoBebida = Body(...)):
    restaurant = jsonable_encoder(restaurant)
    new_restaurant = request.app.database["Recomendacion Alimento Bebida"].insert_one(restaurant)
    created_restaurant = request.app.database["Recomendacion Alimento Bebida"].find_one(
        {"_id": new_restaurant.inserted_id}
    )
    return created_restaurant

# Ruta para consultar todas los rsultados, filtrando el aeropuerto
@router.get("/RecomendacionAlimentoBebida", response_description="Consultar todos los restaurantes", response_model=List[RecomendacionAlimentoBebida])
def list_restaurants(request: Request, airport: str):
    restaurants = list(request.app.database["Recomendacion Alimento Bebida"].find({"airport": {"$gte": airport}}))
    return restaurants

# Ruta para actualizar una ruta del modelo filtrado
@router.put("/RecomendacionAlimentoBebida/{id}", response_description="Actualizar restaurantes por ID", response_model=RecomendacionAlimentoBebida)
def update_restaurant(id: str, request: Request, restaurant: RecomendacionAlimentoBebidaUpdate = Body(...)):
    updated_restaurant = request.app.database["Recomendacion Alimento Bebida"].find_one_and_update(
        {"_id": id},
        {"$set": restaurant.dict(exclude_unset=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_restaurant is not None:
        return updated_restaurant

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")

# Ruta para eliminar una ruta del modelo filtrado
@router.delete("/RecomendacionAlimentoBebida/{id}", response_description="Borrar un restaurante por ID de la base de datos")
def delete_restaurant(id: str, request: Request, response: Response):
    deleted_restaurant = request.app.database["Recomendacion Alimento Bebida"].find_one_and_delete({"_id": id})

    if deleted_restaurant is not None:
        return {"message": f"Ruta con ID {id} eliminada correctamente"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ruta con ID {id} no encontrada")
