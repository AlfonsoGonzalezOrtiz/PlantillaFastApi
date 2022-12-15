from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from config.db import db
from models.model import household, householdUpdate
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

routerhousehold = APIRouter()

collection = "household"

'''CREATE household'''
@routerhousehold.post("/", response_description="Create a new household", status_code=status.HTTP_201_CREATED, response_model=household)
def create_household(request: Request, household: household = Body(...)):
    
    household = jsonable_encoder(household)
    household['stamp'] = datetime.now().timestamp()

    new_household = db[collection].insert_one(household)
    created_household = db[collection].find_one(
        {"_id": new_household.inserted_id}
    )

    return created_household

'''LIST households'''
@routerhousehold.get("/",response_description="List all households", response_model=List[household])
def list_households(request: Request):
    households = list(db[collection].find(limit=100))
    return households
    
'''GET household'''
@routerhousehold.get("/{id}", response_description="Get a single household", response_model=household)
def get_household(id:str, request: Request):
    try:
        if(household := db[collection].find_one({"id": id})) is not None:
            return household
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"household with ID {id} not found")

'''DELETE household'''
@routerhousehold.delete("/{id}", response_description="Delete a household")
def delete_household(id:str, request: Request, response: Response):

    try:
        household_deleted = db[collection].delete_one({"id": id})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"household with ID {id} not found")

    if household_deleted.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"household with ID {id} not found")


'''UPDATE household'''
@routerhousehold.put("/{id}", response_description="Update a household", response_model=household)
def update_household(id:str, request: Request, data: householdUpdate = Body(...)):

    household = {k: v for k, v in data.dict().items() if v is not None}
    household['stamp'] = datetime.now().timestamp()
    
    if len(household) >= 1:
        update_result = db[collection].update_one(
            {"id": id}, {"$set": household}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"household with ID {id} not modified")

    if (
        existing_household := db[collection].find_one({"id":id})
    ) is not None:
        return existing_household

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"household with ID {id} not found")


'''LIST households BY EMAIL'''
@routerhousehold.get("/from/", response_description="Get the list of households by email", response_model=List[household])
def list_households_by_autor(request : Request, response : Response,email: Optional[str] = "/*"):
    households = list(db[collection].find({"vendedor": {"$regex": email}}, limit = 100))
    return households


'''LIST households BY POSITION'''
@routerhousehold.get("/position/{lat}&{lon}", response_description="Get the list of households by position", response_model=List[household])
def list_households_by_autor(lat : float,lon : float, request : Request, response : Response):
    households = list(db[collection].find({"lat": lat,"lon": lon}, limit = 100))
    return households

'''LIST households MORE RECENT THAN'''
@routerhousehold.get("/more_recent/{stamp}", response_description="Get the list of households by position", response_model=List[household])
def list_households_by_autor(stamp : float, request : Request, response : Response):
    households = list(db[collection].find({"stamp":{
        "$gte": stamp
    }}, limit = 100))
    return households
