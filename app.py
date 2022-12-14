from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from routes.exam import routerExam
from routes.test import routerTest

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="Example of description",
    version="0.1.0"
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def redirect(request: Request):
    return RedirectResponse(request.url._url + "docs")

app.include_router(routerTest, tags=["tests"], prefix="/tests")
app.include_router(routerExam, tags=["exam"], prefix="/exams")