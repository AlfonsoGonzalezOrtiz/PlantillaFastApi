from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from config.db import db
from models.model import test, testUpdate
from datetime import datetime

routerTest = APIRouter()

collection = 'tests'
collection2 = 'exam'

'''CREATE TEST'''
@routerTest.post("/", response_description="Create a new test", status_code=status.HTTP_201_CREATED, response_model=test)
def create_test(request: Request, test: test = Body(...)):

    test = jsonable_encoder(test)
    test['stamp'] = datetime.now().timestamp()
    
    #exam_router.create_exam(request,test['exam'])

    new_test = db[collection].insert_one(test)
    created_test = db[collection].find_one(
        {"_id": new_test.inserted_id}
    )

    return created_test

'''LIST TESTS'''
@routerTest.get("/",response_description="List all tests", response_model=List[test])
def list_tests(request: Request):
    tests = list(db[collection].find(limit=100))
    return tests
    
'''GET TEST'''
@routerTest.get("/{id}", response_description="Get a single test", response_model=test)
def get_test(id:str, request: Request):
    try:
        if(test := db[collection].find_one({"_id": ObjectId(id)})) is not None:
            return test
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"test with ID {id} not found")

'''DELETE TEST'''
@routerTest.delete("/{id}", response_description="Delete a test")
def delete_test(id:str, request: Request, response: Response):

    try:
        test_deleted = db[collection].delete_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"test with ID {id} not found")

    if test_deleted.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"test with ID {id} not found")


'''UPDATE TEST'''
@routerTest.put("/{id}", response_description="Update a test", response_model=test)
def update_test(id:str, request: Request, data: testUpdate = Body(...)):

    test = {k: v for k, v in data.dict().items() if v is not None}
    test['stamp'] = datetime.now().timestamp()
    
    if len(test) >= 1:
        update_result = db[collection].update_one(
            {"_id": ObjectId(id)}, {"$set": test}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"test with ID {id} not modified")

    if (
        existing_test := db[collection].find_one({"_id":ObjectId(id)})
    ) is not None:
        return existing_test

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"test with ID {id} not found")


'''LIST TESTS BY EMAIL'''
@routerTest.get("/from/{email}", response_description="Get the list of tests by email", response_model=List[test])
def list_tests_by_autor(email : str, request : Request, response : Response):
    tests = list(db[collection].find({"email": email}, limit = 100))
    return tests


'''LIST TESTS BY POSITION'''
@routerTest.get("/position/{lat}&{lon}", response_description="Get the list of tests by position", response_model=List[test])
def list_tests_by_autor(lat : float,lon : float, request : Request, response : Response):
    tests = list(db[collection].find({"lat": lat,"lon": lon}, limit = 100))
    return tests

'''LIST TESTS MORE RECENT THAN'''
@routerTest.get("/more_recent/{stamp}", response_description="Get the list of tests by position", response_model=List[test])
def list_tests_by_autor(stamp : float, request : Request, response : Response):
    tests = list(db[collection].find({"stamp":{
        "$gte": stamp
    }}, limit = 100))
    return tests