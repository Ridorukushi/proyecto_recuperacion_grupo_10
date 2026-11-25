"""Aplicación FastAPI: CORS, errores en español con la forma {"detalle": ...} y rutas."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import obtener_configuracion
from app.rutas import sitios

app = FastAPI(title="Catálogo de sitios turísticos del Huila", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=obtener_configuracion().origenes,
    allow_methods=["GET"],
    allow_headers=[],
)

_MENSAJES_GENERICOS = {404: "Recurso no encontrado.", 405: "Método no permitido."}


@app.exception_handler(StarletteHTTPException)
async def _error_http(_: Request, error: StarletteHTTPException) -> JSONResponse:
    detalle = _MENSAJES_GENERICOS.get(error.status_code, "No se pudo atender la solicitud.")
    if error.status_code == 422 or (error.status_code == 404 and error.detail != "Not Found"):
        detalle = str(error.detail)
    return JSONResponse({"detalle": detalle}, status_code=error.status_code)


@app.exception_handler(RequestValidationError)
async def _error_validacion(_: Request, __: RequestValidationError) -> JSONResponse:
    return JSONResponse({"detalle": "Los datos enviados no son válidos."}, status_code=422)


app.include_router(sitios.router)
