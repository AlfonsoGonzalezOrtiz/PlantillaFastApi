from typing import Union, List
from pydantic import BaseModel, EmailStr

class Contacto(BaseModel):
    telefono: str
    alias: str

class Usuario(BaseModel):
    telefono: str
    alias: str
    contactos: Union[List[Contacto],None] = None