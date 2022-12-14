from fastapi import APIRouter, Response, status
from config.db import db
from bson import ObjectId
from models.usuario import *
from models.mensaje import Mensaje
from schemas.mensaje import *
from schemas.usuario import *
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.encoders import jsonable_encoder

usuario = APIRouter()
db_document = "usuario"

@usuario.get('/usuarios', response_model=list[Usuario], tags=["usuario"])
async def find_all_usuarios():
    usuarios = usuariosEntity(db[db_document].find())
    return usuarios

@usuario.post('/usuario', response_model=Usuario, tags=["usuario"])
async def insert_usuario(usuario : Usuario):
    nuevo_usuario = jsonable_encoder(usuario)

    id = db[db_document].insert_one(nuevo_usuario).inserted_id
    
    usuario = db[db_document].find_one({"_id" : ObjectId(id) })

    return usuarioEntity(usuario)

@usuario.put('/usuario', response_model=Usuario, tags=["usuario"])
async def update_usuario(id: str, usuario:Usuario):
    db[db_document].find_one_and_update({"_id" : ObjectId(id)}, {"$set": jsonable_encoder(usuario)})
    return usuarioEntity(db[db_document].find_one({"_id" : ObjectId(id) }))

@usuario.delete('/usuario', status_code=HTTP_204_NO_CONTENT, tags=["usuario"])
async def delete_usuario(id: str):
    db[db_document].find_one_and_delete({"_id" : ObjectId(id) })
    return Response(status_code=HTTP_204_NO_CONTENT)
