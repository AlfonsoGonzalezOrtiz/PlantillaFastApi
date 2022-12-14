from fastapi import APIRouter, Response, status #APIRouter: nos permite definir todas las rutas dentro de este archivo
from config.db import db
from bson import ObjectId
from models.mensaje import *
from schemas.usuario import usuarioEntity
from schemas.mensaje import *
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from fastapi.encoders import jsonable_encoder
import json 

mensaje = APIRouter()
db_document = "mensaje"

@mensaje.get('/mensajes', response_model=list[Mensaje],tags=["mensaje"])
async def find_all_mensajes():
    mensajes = mensajesEntity(db[db_document].find().sort("precio", -1))
    return mensajes

@mensaje.post('/mensaje', response_model=Mensaje,tags=["mensaje"])
async def insert_mensaje(mensaje : Mensaje):
    nuevo_mensaje = jsonable_encoder(mensaje)

    nuevo_mensaje["timestamp"]=convertirFecha(nuevo_mensaje["timestamp"])

    id = db[db_document].insert_one(nuevo_mensaje).inserted_id
    
    mensaje = db[db_document].find_one({"_id" : ObjectId(id) })

    return mensajeEntity(mensaje)

@mensaje.put('/mensaje', response_model=Mensaje,tags=["mensaje"])
async def update_mensaje(id: str, mensaje:Mensaje):
    db[db_document].find_one_and_update({"_id" : ObjectId(id)}, {"$set": jsonable_encoder(mensaje)})
    return mensajeEntity(db[db_document].find_one({"_id" : ObjectId(id) }))

@mensaje.delete('/mensaje', status_code=HTTP_204_NO_CONTENT,tags=["mensaje"])
async def delete_mensaje(id: str):
    db[db_document].find_one_and_delete({"_id" : ObjectId(id) })
    return Response(status_code=HTTP_204_NO_CONTENT)

