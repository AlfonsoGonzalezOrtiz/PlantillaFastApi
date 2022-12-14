from typing import Optional,List
from pydantic import BaseModel

class exam(BaseModel):
    email: str
    num: int
    url: List[str]

class examUpdate(BaseModel):
    email: Optional[str]
    num: Optional[int]
    url : Optional[str]

class test(BaseModel):
    email: str
    lat: float
    lon: float
    stamp: Optional[float]
    num: int
    exam: Optional[exam]


class testUpdate(BaseModel):
    email: Optional[str]
    lat:  Optional[float]
    lon: Optional[float]
    stamp: Optional[float]
    num: Optional[int]
    exam: Optional[exam]
