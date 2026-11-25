"""Pruebas de app.carga.cargar_catalogo: reglas de rechazo (CA-17, CA-18 y CA-19)."""

import pytest
from datos_prueba import ELIMINAR, ficha
from sqlalchemy import text


def _cargar_y_fallar(cargar, fichas, patron):
    from app.carga import ErrorCarga

    with pytest.raises(ErrorCarga, match=patron):
        cargar(fichas)


# ---------- CA-17: coordenadas ----------


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("latitud", 1.49999),
        ("latitud", 3.90001),
        ("latitud", 0.0),
        ("longitud", -76.60001),
        ("longitud", -74.39999),
        ("longitud", 0.0),
    ],
)
def test_ca17_coordenadas_fuera_rechazadas(cargar, contar, campo, valor):
    """CA-17: coordenadas fuera del Huila se rechazan y el mensaje nombra el campo; nada se guarda."""
    _cargar_y_fallar(cargar, [ficha(**{campo: valor})], campo)
    assert contar("sitio") == 0


def test_ca17_bordes_aceptados(cargar, contar):
    """CA-17 (límite): los bordes 1.5, 3.9, -76.6 y -74.4 son válidos (inclusivos)."""
    cargar(
        [
            ficha(nombre="Borde sur", latitud=1.5, longitud=-75.0),
            ficha(nombre="Borde norte", latitud=3.9, longitud=-75.0),
            ficha(nombre="Borde oeste", latitud=2.5, longitud=-76.6),
            ficha(nombre="Borde este", latitud=2.5, longitud=-74.4),
        ]
    )
    assert contar("sitio") == 4


# ---------- CA-18: campos obligatorios y listas ----------


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("nombre", ELIMINAR),
        ("nombre", ""),
        ("nombre", "a" * 121),
        ("municipio", ELIMINAR),
        ("municipio", "bogota"),  # no es del Huila
        ("categoria", ELIMINAR),
        ("categoria", "deportes"),  # fuera de las 7
        ("latitud", ELIMINAR),
        ("longitud", ELIMINAR),
        ("fuentes", ELIMINAR),
        ("fuentes", []),
        ("fuentes", ["ftp://example.org/archivo"]),  # no es http/https
        ("descripcion", "x" * 401),
    ],
)
def test_ca18_campos_invalidos_rechazados(cargar, contar, campo, valor):
    """CA-18: una ficha con un campo inválido se rechaza indicando el campo; nada se guarda."""
    _cargar_y_fallar(cargar, [ficha(**{campo: valor})], campo)
    assert contar("sitio") == 0


def test_ca18_limites_de_longitud_aceptados(cargar, contar):
    """CA-18 (límite): nombre de 120, descripción de 400 y concepto de 80 caracteres son válidos."""
    cargar(
        [
            ficha(
                nombre="a" * 120,
                descripcion="d" * 400,
                precios=[{"concepto": "c" * 80, "valor_cop": 1000}],
                fecha_referencia_precio="2026-11-24",
            )
        ]
    )
    assert contar("sitio") == 1
    assert contar("precio") == 1


def test_ca18_todo_o_nada(cargar, sesion, contar):
    """CA-18: si una ficha falla no se guarda ninguna, ni siquiera la válida que iba antes."""
    from app.carga import ErrorCarga

    fichas = [
        ficha(nombre="Válida", precios=[{"concepto": "Entrada", "valor_cop": 5000}],
              fecha_referencia_precio="2026-11-24"),
        ficha(nombre="Inválida", latitud=10.0),
    ]
    with pytest.raises(ErrorCarga, match="latitud"):
        cargar(fichas)
    sesion.rollback()
    assert contar("sitio") == 0
    assert contar("precio") == 0
    assert contar("fuente") == 0


# ---------- CA-19: precios y duplicados ----------


def test_ca19_precio_sin_fecha(cargar, contar):
    """CA-19: un precio conocido sin fecha de consulta se rechaza."""
    fichas = [ficha(precios=[{"concepto": "Entrada", "valor_cop": 25000}],
                    fecha_referencia_precio=None)]
    _cargar_y_fallar(cargar, fichas, "fecha_referencia_precio")
    assert contar("sitio") == 0


def test_ca19_precio_cero_sin_fecha(cargar):
    """CA-19 (límite): un precio 0 (gratis) también es conocido y exige fecha."""
    fichas = [ficha(precios=[{"concepto": "Entrada", "valor_cop": 0}],
                    fecha_referencia_precio=None)]
    _cargar_y_fallar(cargar, fichas, "fecha_referencia_precio")


def test_ca19_precio_desconocido_no_exige_fecha(cargar, contar):
    """CA-19 (límite): si todos los precios son desconocidos (null) no se exige fecha y no se guardan."""
    cargar([ficha(precios=[{"concepto": "Entrada", "valor_cop": None}],
                  fecha_referencia_precio=None)])
    assert contar("sitio") == 1
    assert contar("precio") == 0


@pytest.mark.parametrize("valor", [-1, -25000, 1500.5])
def test_ca19_precio_negativo(cargar, contar, valor):
    """CA-19: un precio negativo (o no entero) se rechaza indicando valor_cop."""
    fichas = [ficha(precios=[{"concepto": "Entrada", "valor_cop": valor}],
                    fecha_referencia_precio="2026-11-24")]
    _cargar_y_fallar(cargar, fichas, "valor_cop")
    assert contar("sitio") == 0


@pytest.mark.parametrize("concepto", ["", "c" * 81])
def test_ca19_concepto_invalido(cargar, concepto):
    """CA-19 (error): concepto de precio vacío o de más de 80 caracteres se rechaza."""
    fichas = [ficha(precios=[{"concepto": concepto, "valor_cop": 1000}],
                    fecha_referencia_precio="2026-11-24")]
    _cargar_y_fallar(cargar, fichas, "concepto")


def test_ca19_nombre_repetido(cargar, contar):
    """CA-19: dos fichas con el mismo nombre se rechazan."""
    fichas = [ficha(nombre="Mismo Nombre"), ficha(nombre="Mismo Nombre")]
    _cargar_y_fallar(cargar, fichas, "nombre|slug")
    assert contar("sitio") == 0


def test_ca19_slug_repetido(cargar, contar):
    """CA-19: nombres distintos que producen el mismo slug también se rechazan."""
    fichas = [ficha(nombre="Café Huila"), ficha(nombre="Cafe  Huila")]
    _cargar_y_fallar(cargar, fichas, "nombre|slug")
    assert contar("sitio") == 0


def test_carga_valida_guarda_sitios_precios_y_fuentes(cargar, sesion, contar):
    """Camino feliz: ficha completa guardada con slug, precios conocidos y todas sus fuentes."""
    cargar(
        [
            ficha(
                nombre="Desierto de la Tatacoa",
                municipio="villavieja",
                precios=[
                    {"concepto": "Entrada adulto", "valor_cop": 25000},
                    {"concepto": "Entrada niño", "valor_cop": None},
                ],
                fecha_referencia_precio="2026-11-24",
                fuentes=["https://example.org/a", "https://example.org/b"],
            )
        ]
    )
    assert contar("municipio") == 5
    assert contar("sitio") == 1
    assert contar("precio") == 1  # el desconocido se descarta
    assert contar("fuente") == 2
    slug = sesion.execute(text("SELECT slug FROM sitio")).scalar_one()
    assert slug == "desierto-de-la-tatacoa"
