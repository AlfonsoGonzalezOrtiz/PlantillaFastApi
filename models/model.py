from typing import Optional,List
from pydantic import BaseModel,Field,EmailStr
import uuid

class parada(BaseModel):
    codLinea: int
    nombreLinea: str
    sentido: int
    orden: Optional[int]
    codParada: Optional[int]
    nombreParada: str
    direccion: Optional[str]
    lat: Optional[float]
    lon: Optional[float]


class paradaUpdate(BaseModel):
    codLinea: Optional[int]
    nombreLinea: Optional[str]
    sentido: Optional[int]
    orden: Optional[int]
    codParada: Optional[int]
    nombreParada: Optional[str]
    direccion: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
