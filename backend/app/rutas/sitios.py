"""GET /api/sitios, /api/sitios/{slug} y /api/filtros (solo lectura)."""

import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import repositorio
from app.catalogos import CATEGORIAS
from app.db import obtener_sesion
from app.esquemas import (
    Filtros,
    Opcion,
    Precio,
    PrecioReferencia,
    SitioDetalle,
    SitioResumen,
)
from app.modelos import Sitio
from app.texto import normalizar

router = APIRouter(prefix="/api")

MAX_BUSQUEDA = 100
MAX_CLAVE = 60
PATRON_CLAVE = re.compile(r"^[a-z0-9-]+$")
PATRON_SLUG =re.compile(r"^[a-z0-9-]{1,120}$")


def _opcion_categoria(clave: str) -> Opcion:
    return Opcion(clave=clave, etiqueta=CATEGORIAS[clave])


def _precio_referencia(sitio: Sitio) -> PrecioReferencia | None:
    if not sitio.precios or sitio.fecha_referencia_precio is None:
        return None
    return PrecioReferencia(
        valor_cop=min(p.valor_cop for p in sitio.precios),
        varios=len(sitio.precios) > 1,
        fecha_referencia_precio=sitio.fecha_referencia_precio,
    )


def _resumen(sitio: Sitio) -> SitioResumen:
    return SitioResumen(
        slug=sitio.slug,
        nombre=sitio.nombre,
        municipio=Opcion(clave=sitio.municipio.clave, etiqueta=sitio.municipio.nombre),
        categoria=_opcion_categoria(sitio.categoria),
        precio_referencia=_precio_referencia(sitio),
    )


def _detalle(sitio: Sitio) -> SitioDetalle:
    return SitioDetalle(
        slug=sitio.slug,
        nombre=sitio.nombre,
        municipio=Opcion(clave=sitio.municipio.clave, etiqueta=sitio.municipio.nombre),
        categoria=_opcion_categoria(sitio.categoria),
        descripcion=sitio.descripcion,
        latitud=sitio.latitud,
        longitud=sitio.longitud,
        horario=sitio.horario,
        como_llegar=sitio.como_llegar,
        precios=[Precio(concepto=p.concepto, valor_cop=p.valor_cop) for p in sitio.precios],
        fecha_referencia_precio=sitio.fecha_referencia_precio,
        fuentes=[f.url for f in sitio.fuentes],
    )


@router.get(
    "/sitios",
    response_model=list[SitioResumen],
    responses={422: {"description": "Municipio, categoría o búsqueda inválidos."}},
)
def listar_sitios(
    sesion: Annotated[Session, Depends(obtener_sesion)],
    municipio: Annotated[str | None, Query()] = None,
    categoria: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query()] = None,
):
    if q is not None:
        if len(q) > MAX_BUSQUEDA:
            raise HTTPException(422, f"El parámetro «q» no puede superar los {MAX_BUSQUEDA} caracteres.")
        if any(ord(c) < 32 or ord(c) == 127 for c in q):
            raise HTTPException(422, "El parámetro «q» contiene caracteres no permitidos.")
    for nombre, valor in (("municipio", municipio), ("categoria", categoria)):
        if valor and (len(valor) > MAX_CLAVE or not PATRON_CLAVE.fullmatch(valor)):
            raise HTTPException(
                422,
                f"El parámetro «{nombre}» no es válido: use hasta {MAX_CLAVE} caracteres "
                "entre minúsculas, números y guiones.",
            )
    if categoria and categoria not in CATEGORIAS:
        raise HTTPException(
            422,
            f"El parámetro «categoria» tiene un valor no válido: «{categoria}». "
            f"Valores permitidos: {', '.join(CATEGORIAS)}.",
        )
    if municipio and municipio not in {m.clave for m in repositorio.listar_municipios(sesion)}:
        raise HTTPException(422, f"El municipio «{municipio}» no existe en el Huila.")
    return [_resumen(s) for s in repositorio.listar_sitios(sesion, municipio, categoria, q)]


@router.get(
    "/sitios/{slug}",
    response_model=SitioDetalle,
    responses={404: {"description": "Sitio no encontrado."}},
)
def obtener_sitio(slug: str, sesion: Annotated[Session, Depends(obtener_sesion)]):
    sitio = repositorio.obtener_sitio(sesion, slug) if PATRON_SLUG.fullmatch(slug) else None
    if sitio is None:
        raise HTTPException(404, "Sitio no encontrado.")
    return _detalle(sitio)


@router.get("/filtros", response_model=Filtros)
def obtener_filtros(sesion: Annotated[Session, Depends(obtener_sesion)]):
    municipios = sorted(repositorio.listar_municipios(sesion), key=lambda m: normalizar(m.nombre))
    categorias = sorted(CATEGORIAS.items(), key=lambda par: normalizar(par[1]))
    return Filtros(
        municipios=[Opcion(clave=m.clave, etiqueta=m.nombre) for m in municipios],
        categorias=[Opcion(clave=c, etiqueta=e) for c, e in categorias],
    )
