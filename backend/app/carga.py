"""Carga del catálogo desde backend/datos/: todo o nada (research D10).

Uso manual: `cd backend && uv run python -m app.carga` (recrea las tablas y carga el catálogo completo).
"""

import json
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.config import RAIZ_BACKEND, obtener_configuracion
from app.esquemas import FichaSitio
from app.modelos import Fuente, Municipio, Precio, Sitio
from app.texto import normalizar, slug

DATOS = RAIZ_BACKEND / "datos"


class ErrorCarga(Exception):
    """Una o más fichas incumplen las reglas de datos; no se guardó nada."""

    def __init__(self, errores: list[str]):
        self.errores = errores
        super().__init__("\n".join(errores))


def _etiqueta(ficha: object, indice: int) -> str:
    nombre = ficha.get("nombre") if isinstance(ficha, dict) else None
    return f"«{nombre}»" if isinstance(nombre, str) and nombre.strip() else f"ficha {indice + 1}"


def _mensajes(etiqueta: str, error: ValidationError) -> list[str]:
    mensajes = []
    for e in error.errors():
        campo = ".".join(str(parte) for parte in e["loc"])
        mensajes.append(f"{etiqueta}: {campo}: {e['msg']}" if campo else f"{etiqueta}: {e['msg']}")
    return mensajes


def cargar_catalogo(sesion: Session, ruta_sitios: Path, ruta_municipios: Path) -> None:
    """Valida todas las fichas y las agrega a la sesión. No confirma (commit); la persona que llama lo hace."""
    municipios = json.loads(Path(ruta_municipios).read_text(encoding="utf-8"))["municipios"]
    claves = {m["clave"] for m in municipios}
    crudas = json.loads(Path(ruta_sitios).read_text(encoding="utf-8"))

    errores: list[str] = []
    fichas: list[FichaSitio] = []
    nombres: set[str] = set()
    slugs: set[str] = set()
    for i, cruda in enumerate(crudas):
        etiqueta = _etiqueta(cruda, i)
        try:
            ficha = FichaSitio.model_validate(cruda)
        except ValidationError as error:
            errores.extend(_mensajes(etiqueta, error))
            continue
        if ficha.municipio not in claves:
            errores.append(f"{etiqueta}: municipio: «{ficha.municipio}» no es un municipio del Huila")
        if ficha.nombre in nombres:
            errores.append(f"{etiqueta}: nombre: repetido")
        if slug(ficha.nombre) in slugs:
            errores.append(f"{etiqueta}: slug: repetido («{slug(ficha.nombre)}»)")
        nombres.add(ficha.nombre)
        slugs.add(slug(ficha.nombre))
        fichas.append(ficha)

    if errores:
        raise ErrorCarga(errores)

    sesion.add_all(Municipio(clave=m["clave"], nombre=m["nombre"]) for m in municipios)
    for ficha in fichas:
        conocidos = ficha.precios_conocidos
        sesion.add(
            Sitio(
                slug=slug(ficha.nombre),
                nombre=ficha.nombre,
                nombre_normalizado=normalizar(ficha.nombre),
                municipio_clave=ficha.municipio,
                categoria=ficha.categoria,
                descripcion=ficha.descripcion,
                latitud=ficha.latitud,
                longitud=ficha.longitud,
                horario=ficha.horario,
                como_llegar=ficha.como_llegar,
                fecha_referencia_precio=ficha.fecha_referencia_precio if conocidos else None,
                precios=[Precio(concepto=p.concepto, valor_cop=p.valor_cop) for p in conocidos],
                fuentes=[Fuente(url=url) for url in ficha.fuentes],
            )
        )
    sesion.flush()


def _principal() -> None:
    from app.db import crear_esquema, crear_motor

    motor = crear_motor(obtener_configuracion().database_url)
    crear_esquema(motor)
    with Session(motor) as sesion:
        try:
            cargar_catalogo(sesion, DATOS / "sitios.json", DATOS / "municipios.json")
        except ErrorCarga as error:
            raise SystemExit(f"No se cargó nada:\n{error}") from error
        sesion.commit()
    print("Catálogo cargado.")


if __name__ == "__main__":
    _principal()
