from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from config.db import db
from models.model import parada, paradaUpdate
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

routerparada = APIRouter()

collection = "parada"

'''CREATE parada'''
@routerparada.post("/", response_description="Create a new parada", status_code=status.HTTP_201_CREATED, response_model=parada)
def create_parada(request: Request, parada: parada = Body(...)):
    
    parada = jsonable_encoder(parada)

    new_parada = db[collection].insert_one(parada)
    created_parada = db[collection].find_one(
        {"_id": new_parada.inserted_id}
    )

    return created_parada

'''LIST paradas'''
@routerparada.get("/",response_description="List all paradas", response_model=List[parada])
def list_paradas(request: Request):
    paradas = list(db[collection].find(limit=100))
    return paradas
    
'''GET parada'''
@routerparada.get("/{codParada}", response_description="Get a single parada", response_model=parada)
def get_parada(codParada:int, request: Request):
    try:
        if(parada := db[collection].find_one({"codParada": codParada})) is not None:
            return parada
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"parada with ID {id} not found")

'''DELETE parada'''
@routerparada.delete("/{codParada}", response_description="Delete a parada")
def delete_parada(codParada:int, request: Request, response: Response):

    try:
        parada_deleted = db[collection].delete_one({"codParada": codParada})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"parada with ID {codParada} not found")

    if parada_deleted.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"parada with ID {codParada} not found")


'''UPDATE parada'''
@routerparada.put("/{codParada}", response_description="Update a parada", response_model=parada)
def update_parada(codParada:int, request: Request, data: paradaUpdate = Body(...)):

    parada = {k: v for k, v in data.dict().items() if v is not None}
    
    if len(parada) >= 1:
        update_result = db[collection].update_one(
            {"codParada": codParada}, {"$set": parada}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"parada with ID {codParada} not modified")

    if (
        existing_parada := db[collection].find_one({"codParada":codParada})
    ) is not None:
        return existing_parada

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"parada with ID {codParada} not found")


'''LIST paradas BY POSITION'''
@routerparada.get("/position/{lat}&{lon}", response_description="Get the list of paradas by position", response_model=List[parada])
def list_paradas_by_position(lat : float,lon : float, request : Request, response : Response):
    paradas = list(db[collection].find({"lat": lat,"lon": lon}, limit = 100))
    return paradas

'''LIST paradas por sentido y linea'''
@routerparada.get("/sentido/{sentido}/linea/{linea}", response_description="Get the list of paradas by line and direction", response_model=List[parada])
def list_paradas_by_sentidoylinea(sentido : int,linea : int, request : Request, response : Response):
    paradas = list(db[collection].find({"sentido": sentido,"codLinea": linea}, limit = 100))
    return paradas
