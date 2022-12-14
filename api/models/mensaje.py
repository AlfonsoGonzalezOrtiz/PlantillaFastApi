from typing import Union, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Mensaje(BaseModel):
    timestamp: datetime 
    origen: str
    destino: str
    texto: str = Field(None, max_length=400)