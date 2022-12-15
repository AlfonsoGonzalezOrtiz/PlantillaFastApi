from typing import Optional,List
from pydantic import BaseModel,Field,EmailStr
import uuid

class book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    household: str
    comprador: EmailStr
    stamp: Optional[float]
    cantidad: float

class bookUpdate(BaseModel):
    household: Optional[str]
    comprador: Optional[EmailStr]
    stamp: Optional[float]
    cantidad: Optional[float]

class household(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    vendedor: Optional[EmailStr]
    description: Optional[str]
    num: Optional[float]
    photos: Optional[List[str]]
    lat: Optional[float]
    lon: Optional[float]
    stamp: Optional[float]
    comprador: Optional[EmailStr]


class householdUpdate(BaseModel):
    vendedor: Optional[EmailStr]
    description: Optional[str]
    num: Optional[float]
    photos: Optional[List[str]]
    lat: Optional[float]
    lon: Optional[float]
    stamp: Optional[float]
    comprador: Optional[EmailStr]
