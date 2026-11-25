"""Carga del catálogo desde backend/datos/: todo o nada (research D10).

Uso manual: `cd backend && uv run python -m app.carga` (recrea las tablas y carga el catálogo completo).
"""

import json
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy import Engine, text
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
    if isinstance(nombre, str) and nombre.strip():
        return f"«{nombre.strip()[:60]}»"
    return f"«ficha {indice + 1}»"


_ENTERO = "debe ser un número entero"
_NUMERO = "debe ser un número"
_FECHA = "debe ser una fecha válida (AAAA-MM-DD)"

_PLANTILLAS = {
    "missing": lambda c: "obligatorio",
    "string_too_long": lambda c: f"no puede superar {c.get('max_length')} caracteres",
    "string_too_short": lambda c: f"debe tener al menos {c.get('min_length')} caracteres",
    "too_long": lambda c: f"no puede tener más de {c.get('max_length')} elementos",
    "too_short": lambda c: f"debe tener al menos {c.get('min_length')} elemento(s)",
    "less_than_equal": lambda c: f"debe ser menor o igual a {c.get('le')}",
    "greater_than_equal": lambda c: f"debe ser mayor o igual a {c.get('ge')}",
    "int_type": lambda c: _ENTERO,
    "int_from_float": lambda c: _ENTERO,
    "int_parsing": lambda c: _ENTERO,
    "float_type": lambda c: _NUMERO,
    "float_parsing": lambda c: _NUMERO,
    "string_type": lambda c: "debe ser un texto",
    "list_type": lambda c: "debe ser una lista",
    "date_type": lambda c: _FECHA,
    "date_parsing": lambda c: _FECHA,
    "date_from_datetime_parsing": lambda c: _FECHA,
    "literal_error": lambda c: "no es un valor permitido",
}


def _traducir(error: dict) -> str:
    """Mensaje en español según el tipo de error de Pydantic."""
    tipo = error["type"]
    if tipo == "value_error":
        return str(error["msg"]).removeprefix("Value error, ")
    plantilla = _PLANTILLAS.get(tipo)
    return plantilla(error.get("ctx") or {}) if plantilla else "valor no válido"


def _mensajes(etiqueta: str, error: ValidationError) -> list[str]:
    mensajes = []
    for e in error.errors():
        campo = ".".join(str(parte) for parte in e["loc"])
        texto = _traducir(e)
        mensajes.append(f"{etiqueta}: {campo}: {texto}" if campo else f"{etiqueta}: {texto}")
    return mensajes


def _validar_ficha(cruda: object, indice: int, claves: set[str], vistos: tuple[set, set]):
    """Devuelve (ficha o None, lista de errores)."""
    nombres, slugs = vistos
    etiqueta = _etiqueta(cruda, indice)
    try:
        ficha = FichaSitio.model_validate(cruda)
    except ValidationError as error:
        return None, _mensajes(etiqueta, error)
    errores: list[str] = []
    if ficha.municipio not in claves:
        errores.append(f"{etiqueta}: municipio: «{ficha.municipio}» no es un municipio del Huila")
    mi_slug = slug(ficha.nombre)
    if not mi_slug:
        errores.append(f"{etiqueta}: nombre: debe tener al menos una letra o un número")
        return None, errores
    if ficha.nombre in nombres:
        errores.append(f"{etiqueta}: nombre: repetido")
    elif mi_slug in slugs:
        errores.append(f"{etiqueta}: slug: repetido («{mi_slug}»)")
    nombres.add(ficha.nombre)
    slugs.add(mi_slug)
    return ficha, errores


def validar_catalogo(ruta_sitios: Path, ruta_municipios: Path) -> tuple[list[dict], list[FichaSitio]]:
    """Lee y valida todo sin tocar la base. Lanza ErrorCarga con todos los errores."""
    municipios = json.loads(Path(ruta_municipios).read_text(encoding="utf-8"))["municipios"]
    claves = {m["clave"] for m in municipios}
    crudas = json.loads(Path(ruta_sitios).read_text(encoding="utf-8"))

    errores: list[str] = []
    fichas: list[FichaSitio] = []
    vistos: tuple[set, set] = (set(), set())
    for i, cruda in enumerate(crudas):
        ficha, errores_ficha = _validar_ficha(cruda, i, claves, vistos)
        errores.extend(errores_ficha)
        if ficha is not None:
            fichas.append(ficha)

    if errores:
        raise ErrorCarga(errores)
    return municipios, fichas


def cargar_catalogo(sesion: Session, ruta_sitios: Path, ruta_municipios: Path) -> None:
    """Valida todas las fichas y las agrega a la sesión. No confirma (commit); la persona que llama lo hace."""
    municipios, fichas = validar_catalogo(ruta_sitios, ruta_municipios)

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


def reemplazar_catalogo(motor: Engine, ruta_sitios: Path, ruta_municipios: Path) -> None:
    """Reemplaza el catálogo completo en una sola transacción.

    Valida primero (sin tocar la base); si algo falla, la transacción se revierte y nada cambia.
    """
    validar_catalogo(ruta_sitios, ruta_municipios)
    with motor.begin() as conexion:
        conexion.execute(text("TRUNCATE precio, fuente, sitio, municipio RESTART IDENTITY CASCADE"))
        with Session(bind=conexion) as sesion:
            cargar_catalogo(sesion, ruta_sitios, ruta_municipios)


def _principal() -> None:
    from app.db import asegurar_esquema, crear_motor

    motor = crear_motor(obtener_configuracion().database_url)
    asegurar_esquema(motor)
    try:
        reemplazar_catalogo(motor, DATOS / "sitios.json", DATOS / "municipios.json")
    except ErrorCarga as error:
        raise SystemExit(f"No se cargó nada:\n{error}") from error
    print("Catálogo cargado.")


if __name__ == "__main__":
    _principal()
