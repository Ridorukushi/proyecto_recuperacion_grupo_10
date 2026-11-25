"""Datos y ayudas propias de las pruebas (no son los datos reales de backend/datos/)."""

import json
from pathlib import Path

# Valor especial: en `ficha(...)` quita el campo en vez de ponerle un valor.
ELIMINAR = object()


def ficha(**cambios):
    """Ficha válida mínima; `cambios` reemplaza o (con ELIMINAR) quita campos."""
    base = {
        "nombre": "Sitio de Prueba",
        "municipio": "neiva",
        "categoria": "naturaleza",
        "descripcion": "Descripción de prueba.",
        "latitud": 2.9,
        "longitud": -75.3,
        "precios": [],
        "fecha_referencia_precio": None,
        "horario": None,
        "como_llegar": None,
        "fuentes": ["https://example.org/fuente"],
    }
    for campo, valor in cambios.items():
        if valor is ELIMINAR:
            base.pop(campo, None)
        else:
            base[campo] = valor
    return base


MUNICIPIOS_SEMILLA = {
    "fuente": "https://example.org/municipios",
    "municipios": [
        {"clave": "neiva", "nombre": "Neiva"},
        {"clave": "garzon", "nombre": "Garzón"},
        {"clave": "villavieja", "nombre": "Villavieja"},
        {"clave": "san-agustin", "nombre": "San Agustín"},
        {"clave": "pitalito", "nombre": "Pitalito"},  # sin sitios a propósito
    ],
}

# Siete sitios de prueba. Orden alfabético esperado (por nombre sin tildes ni mayúsculas):
# Ágora, Balneario, Desierto, Malecón, Observatorio, Parque, Santuario.
SITIOS_SEMILLA = [
    ficha(
        nombre="Desierto de la Tatacoa",
        municipio="villavieja",
        categoria="naturaleza",
        descripcion="Zona árida de prueba con cielos despejados.",
        latitud=3.2333,
        longitud=-75.1667,
        horario="Todos los días, 24 horas",
        como_llegar="Desde Neiva por la vía a Villavieja.",
        precios=[
            {"concepto": "Entrada adulto", "valor_cop": 25000},
            {"concepto": "Entrada niño", "valor_cop": 15000},
        ],
        fecha_referencia_precio="2026-11-24",
        fuentes=["https://example.org/tatacoa-a", "https://example.org/tatacoa-b"],
    ),
    ficha(
        nombre="Parque Arqueológico de San Agustín",
        municipio="san-agustin",
        categoria="arqueologia",
        descripcion="Parque de prueba con estatuas.",
        latitud=1.8855,
        longitud=-76.2765,
        horario="8:00 a 16:00",
        como_llegar="Por la vía Pitalito - San Agustín.",
        precios=[{"concepto": "Entrada general", "valor_cop": 30000}],
        fecha_referencia_precio="2026-11-24",
        fuentes=["https://example.org/parque"],
    ),
    ficha(
        nombre="Balneario Termal Los Lagos",
        municipio="neiva",
        categoria="termales",
        descripcion=None,
        latitud=2.93,
        longitud=-75.28,
        precios=[],
        fuentes=["https://example.org/balneario"],
    ),
    ficha(
        nombre="Malecón de Neiva",
        municipio="neiva",
        categoria="cultura",
        descripcion="Paseo de prueba junto al río.",
        latitud=2.9273,
        longitud=-75.2819,
        horario="Abierto todo el día",
        precios=[{"concepto": "Entrada", "valor_cop": 0}],
        fecha_referencia_precio="2026-11-24",
        fuentes=["https://example.org/malecon"],
    ),
    ficha(
        nombre="Santuario de Garzón",
        municipio="garzon",
        categoria="religioso",
        descripcion="Templo de prueba.",
        latitud=2.1964,
        longitud=-75.6272,
        precios=[
            {"concepto": "Entrada adulto", "valor_cop": 0},
            {"concepto": "Visita guiada", "valor_cop": 8000},
        ],
        fecha_referencia_precio="2026-11-24",
        fuentes=["https://example.org/santuario"],
    ),
    ficha(
        nombre="Observatorio Astronómico de la Tatacoa",
        municipio="villavieja",
        categoria="cultura",
        descripcion="Observatorio de prueba.",
        latitud=3.2331,
        longitud=-75.1699,
        precios=[
            {"concepto": "Entrada", "valor_cop": 12000},
            {"concepto": "Sesión nocturna", "valor_cop": None},  # desconocido: se descarta
        ],
        fecha_referencia_precio="2026-10-15",
        fuentes=["https://example.org/observatorio"],
    ),
    ficha(
        nombre="Ágora Cultural de Neiva",
        municipio="neiva",
        categoria="cultura",
        descripcion="Centro cultural de prueba.",
        latitud=2.9301,
        longitud=-75.2899,
        precios=[{"concepto": "Entrada", "valor_cop": None}],  # único precio desconocido
        fecha_referencia_precio=None,
        fuentes=["https://example.org/agora"],
    ),
]


def escribir_json(carpeta: Path, fichas, municipios=None):
    """Escribe sitios.json y municipios.json temporales; devuelve (ruta_sitios, ruta_municipios)."""
    ruta_sitios = carpeta / "sitios.json"
    ruta_municipios = carpeta / "municipios.json"
    ruta_sitios.write_text(json.dumps(fichas, ensure_ascii=False), encoding="utf-8")
    ruta_municipios.write_text(
        json.dumps(MUNICIPIOS_SEMILLA if municipios is None else municipios, ensure_ascii=False),
        encoding="utf-8",
    )
    return ruta_sitios, ruta_municipios
