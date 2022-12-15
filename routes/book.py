from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from config.db import db
from models.model import book, bookUpdate

routerbook = APIRouter()

collection = 'book'

'''CREATE book'''
@routerbook.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=book)
def create_book(request: Request, book: book = Body(...)):

    book = jsonable_encoder(book)
    new_book = db[collection].insert_one(book)
    created_book = db[collection].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book

'''LIST bookings'''
@routerbook.get("/",response_description="List all bookings", response_model=List[book])
def list_bookings(request: Request):
    bookings = list(db[collection].find(limit=100))
    return bookings
    
'''GET book'''
@routerbook.get("/{id}", response_description="Get a single book", response_model=book)
def get_book(id:str, request: Request):
    
        if(book := db[collection].find_one({"id": id})) is not None:
            return book

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")


'''DELETE book'''
@routerbook.delete("/{id}", response_description="Delete a book")
def delete_book(id:str, request: Request, response: Response):

    try:
        book_deleted = db[collection].delete_one({"id": id})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")

    if book_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")


'''UPDATE book'''
@routerbook.put("/{id}", response_description="Update a book", response_model=book)
def update_book(id:str, request: Request, data: bookUpdate = Body(...)):

    book = {k: v for k, v in data.dict().items() if v is not None}
    
    if len(book) >= 1:
        update_result = db[collection].update_one(
            {"id": id}, {"$set": book}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not modified")

    if (
        existing_book := db[collection].find_one({"id":id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")

"""
'''LIST bookings BY EMAIL'''
@routerbook.get("/from/{email}", response_description="Get the list of bookings by email", response_model=List[book])
def list_bookings_by_autor(email : str, request : Request, response : Response):
    bookings = list(db[collection].find({"email": email}, limit = 100))
    return bookings
"""