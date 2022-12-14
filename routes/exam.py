from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from config.db import db
from models.model import exam, examUpdate

routerExam = APIRouter()

collection = 'exam'

'''CREATE exam'''
@routerExam.post("/", response_description="Create a new exam", status_code=status.HTTP_201_CREATED, response_model=exam)
def create_exam(request: Request, exam: exam = Body(...)):

    exam = jsonable_encoder(exam)
    new_exam = db[collection].insert_one(exam)
    created_exam = db[collection].find_one(
        {"_id": new_exam.inserted_id}
    )

    return created_exam

'''LIST exams'''
@routerExam.get("/",response_description="List all exams", response_model=List[exam])
def list_exams(request: Request):
    exams = list(db[collection].find(limit=100))
    return exams
    
'''GET exam'''
@routerExam.get("/{id}", response_description="Get a single exam", response_model=exam)
def get_exam(id:str, request: Request):
    
        if(exam := db[collection].find_one({"_id": ObjectId(id)})) is not None:
            return exam

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with ID {id} not found")


'''DELETE exam'''
@routerExam.delete("/{id}", response_description="Delete a exam")
def delete_exam(id:str, request: Request, response: Response):

    try:
        exam_deleted = db[collection].delete_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with ID {id} not found")

    if exam_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with ID {id} not found")


'''UPDATE exam'''
@routerExam.put("/{id}", response_description="Update a exam", response_model=exam)
def update_exam(id:str, request: Request, data: examUpdate = Body(...)):

    exam = {k: v for k, v in data.dict().items() if v is not None}
    
    if len(exam) >= 1:
        update_result = db[collection].update_one(
            {"_id": ObjectId(id)}, {"$set": exam}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with ID {id} not modified")

    if (
        existing_exam := db[collection].find_one({"_id":ObjectId(id)})
    ) is not None:
        return existing_exam

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with ID {id} not found")


'''LIST exams BY EMAIL'''
@routerExam.get("/from/{email}", response_description="Get the list of exams by email", response_model=List[exam])
def list_exams_by_autor(email : str, request : Request, response : Response):
    exams = list(db[collection].find({"email": email}, limit = 100))
    return exams
