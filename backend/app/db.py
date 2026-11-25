"""Motor, sesión por petición y creación del esquema."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import RAIZ_BACKEND, obtener_configuracion

RUTA_ESQUEMA = RAIZ_BACKEND / "db" / "001_esquema.sql"


def crear_motor(url: str) -> Engine:
    return create_engine(url)


def crear_esquema(motor: Engine) -> None:
    """Borra y recrea las tablas con backend/db/001_esquema.sql."""
    sql = RUTA_ESQUEMA.read_text(encoding="utf-8")
    with motor.begin() as conexion:
        conexion.exec_driver_sql(sql)


@lru_cache
def _motor_de_la_aplicacion() -> Engine:
    return crear_motor(obtener_configuracion().database_url)


def obtener_sesion() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por petición."""
    with Session(_motor_de_la_aplicacion()) as sesion:
        yield sesion
