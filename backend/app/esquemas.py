"""Esquemas Pydantic: ficha de carga (FichaSitio) y respuestas de la API."""

from datetime import date
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    StrictInt,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.catalogos import CATEGORIAS

# ---------- Carga (backend/datos/sitios.json) ----------


class PrecioFicha(BaseModel):
    concepto: Annotated[str, StringConstraints(min_length=1, max_length=80)]
    valor_cop: StrictInt | None = Field(default=None, ge=0)  # None = desconocido


class FichaSitio(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
    municipio: str
    categoria: str
    descripcion: Annotated[str, StringConstraints(max_length=400)] | None = None
    latitud: float = Field(ge=1.5, le=3.9)
    longitud: float = Field(ge=-76.6, le=-74.4)
    precios: list[PrecioFicha] = []
    fecha_referencia_precio: date | None = None
    horario: str | None = None
    como_llegar: str | None = None
    fuentes: list[str] = Field(min_length=1)

    @field_validator("categoria")
    @classmethod
    def _categoria_permitida(cls, valor: str) -> str:
        if valor not in CATEGORIAS:
            raise ValueError(f"«{valor}» no es una categoría permitida ({', '.join(CATEGORIAS)})")
        return valor

    @field_validator("fuentes")
    @classmethod
    def _fuentes_http(cls, urls: list[str]) -> list[str]:
        for url in urls:
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"la fuente «{url}» debe empezar por http:// o https://")
        return urls

    @model_validator(mode="after")
    def _fecha_si_hay_precios(self) -> "FichaSitio":
        if self.precios_conocidos and self.fecha_referencia_precio is None:
            raise ValueError("fecha_referencia_precio es obligatoria cuando hay precios conocidos")
        return self

    @property
    def precios_conocidos(self) -> list[PrecioFicha]:
        return [p for p in self.precios if p.valor_cop is not None]


# ---------- Respuestas de la API ----------


class Opcion(BaseModel):
    clave: str
    etiqueta: str


class PrecioReferencia(BaseModel):
    valor_cop: int
    varios: bool
    fecha_referencia_precio: date


class SitioResumen(BaseModel):
    slug: str
    nombre: str
    municipio: Opcion
    categoria: Opcion
    precio_referencia: PrecioReferencia | None


class Precio(BaseModel):
    concepto: str
    valor_cop: int


class SitioDetalle(BaseModel):
    slug: str
    nombre: str
    municipio: Opcion
    categoria: Opcion
    descripcion: str | None
    latitud: float
    longitud: float
    horario: str | None
    como_llegar: str | None
    precios: list[Precio]
    fecha_referencia_precio: date | None
    fuentes: list[str]


class Filtros(BaseModel):
    municipios: list[Opcion]
    categorias: list[Opcion]
