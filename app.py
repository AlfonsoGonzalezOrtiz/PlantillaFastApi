from fastapi.responses import RedirectResponse

from fastapi import FastAPI, Request
from routes.mensaje import mensaje
from routes.usuario import usuario

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="Example of description",
    version="0.1.0"
)

@app.get("/", include_in_schema=False)
async def redirect(request: Request):
    return RedirectResponse(request.url._url + "docs")

app.include_router(mensaje) #me incluye todas las rutas definidas para el usuario
app.include_router(usuario)