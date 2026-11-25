"""Fixtures compartidas: base PostgreSQL de pruebas, sesión, cargador de fichas y TestClient.

Los módulos de `app` se importan dentro de las fixtures (no arriba) para que cada archivo de prueba
falle por su propio motivo mientras el código no exista.
"""

import os
from pathlib import Path

import pytest
from datos_prueba import SITIOS_SEMILLA, escribir_json
from dotenv import dotenv_values

RAIZ_BACKEND = Path(__file__).resolve().parent.parent


def _url_pruebas() -> str:
    url = os.environ.get("DATABASE_URL_PRUEBAS")
    if not url:
        url = dotenv_values(RAIZ_BACKEND / ".env").get("DATABASE_URL_PRUEBAS")
    if not url:
        pytest.fail("Falta DATABASE_URL_PRUEBAS (entorno o backend/.env) para las pruebas con PostgreSQL.")
    # R6: las pruebas borran tablas; nunca deben correr contra una base que no sea de pruebas.
    nombre_base = url.rsplit("/", 1)[-1].split("?")[0]
    if "prueba" not in nombre_base.lower():
        pytest.fail(
            f"La base «{nombre_base}» no parece de pruebas (su nombre debe contener «prueba»). "
            "Las pruebas borran datos: se niegan a correr."
        )
    return url


@pytest.fixture(scope="session")
def motor():
    """Motor de la base de pruebas con el esquema recién creado (una vez por sesión de pruebas)."""
    from app.db import crear_esquema, crear_motor

    motor = crear_motor(_url_pruebas())
    crear_esquema(motor)
    yield motor
    motor.dispose()


@pytest.fixture
def bd_limpia(motor):
    """Deja las tablas vacías antes de cada prueba."""
    from sqlalchemy import text

    with motor.begin() as conexion:
        conexion.execute(text("TRUNCATE precio, fuente, sitio, municipio RESTART IDENTITY CASCADE"))
    return motor


@pytest.fixture
def sesion(bd_limpia):
    from sqlalchemy.orm import Session

    with Session(bd_limpia) as s:
        yield s


@pytest.fixture
def contar(bd_limpia):
    """Función que cuenta filas de una tabla desde una conexión nueva (solo lo ya confirmado)."""
    from sqlalchemy import text

    def _contar(tabla: str) -> int:
        with bd_limpia.connect() as conexion:
            return conexion.execute(text(f"SELECT count(*) FROM {tabla}")).scalar_one()

    return _contar


@pytest.fixture
def cargar(sesion, tmp_path):
    """Función `cargar(fichas, municipios=None)`: escribe JSON temporales y llama a cargar_catalogo."""
    from app.carga import cargar_catalogo

    def _cargar(fichas, municipios=None):
        ruta_sitios, ruta_municipios = escribir_json(tmp_path, fichas, municipios)
        cargar_catalogo(sesion, ruta_sitios, ruta_municipios)
        sesion.commit()

    return _cargar


@pytest.fixture
def catalogo_semilla(cargar):
    """Carga los 7 sitios de prueba (y sus 5 municipios) en la base."""
    cargar(SITIOS_SEMILLA)


@pytest.fixture
def cliente(bd_limpia):
    """TestClient con la dependencia de sesión apuntando a la base de pruebas."""
    from fastapi.testclient import TestClient
    from sqlalchemy.orm import Session

    from app.db import obtener_sesion
    from app.main import app

    def _sesion_de_prueba():
        with Session(bd_limpia) as s:
            yield s

    app.dependency_overrides[obtener_sesion] = _sesion_de_prueba
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(obtener_sesion, None)
