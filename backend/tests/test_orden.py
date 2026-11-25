"""Pruebas de la spec 002: parámetro `orden` de GET /api/sitios (nombre | precio).

Usan sitios semilla propios, insertados a propósito en un orden que no es ni alfabético ni por precio.
Precios de referencia: Cascada 20000, Mirador 10000, Laguna 15000, Zona 0 (gratis), Rio y Plaza 12000 (empate),
Zorro y Castillo sin precio.
"""

import pytest
from datos_prueba import ficha


def _con_precio(valor):
    return {"precios": [{"concepto": "Entrada", "valor_cop": valor}], "fecha_referencia_precio": "2026-11-24"}


SITIOS_ORDEN = [
    ficha(nombre="Cascada Veinte", municipio="neiva", **_con_precio(20000)),
    ficha(nombre="Mirador Diez", municipio="villavieja", **_con_precio(10000)),
    ficha(nombre="Laguna Quince", municipio="neiva", **_con_precio(15000)),
    ficha(nombre="Zona Gratis", municipio="neiva", **_con_precio(0)),
    ficha(nombre="Rio Alfa", municipio="garzon", **_con_precio(12000)),
    ficha(nombre="Plaza Beta", municipio="neiva", **_con_precio(12000)),
    ficha(nombre="Zorro Sin Precio", municipio="neiva", precios=[]),
    ficha(nombre="Castillo Sin Precio", municipio="villavieja", precios=[]),
]


@pytest.fixture
def catalogo_orden(cargar):
    cargar(SITIOS_ORDEN)


def _slugs(respuesta):
    assert respuesta.status_code == 200
    return [s["slug"] for s in respuesta.json()]


def test_ca1_ordena_por_precio_de_menor_a_mayor(cliente, catalogo_orden):
    """CA-1: los sitios con precio salen de menor a mayor (10000, 12000, 12000, 15000, 20000)."""
    r = cliente.get("/api/sitios", params={"orden": "precio"})
    assert r.status_code == 200
    con_precio = [s["precio_referencia"]["valor_cop"] for s in r.json() if s["precio_referencia"]]
    assert con_precio == [0, 10000, 12000, 12000, 15000, 20000]
    assert _slugs(r) == [
        "zona-gratis",
        "mirador-diez",
        "plaza-beta",
        "rio-alfa",
        "laguna-quince",
        "cascada-veinte",
        "castillo-sin-precio",
        "zorro-sin-precio",
    ]


def test_ca2_sin_precio_al_final_por_nombre(cliente, catalogo_orden):
    """CA-2: los sin precio van después de todos los que tienen, ordenados por nombre (Castillo antes que Zorro)."""
    slugs = _slugs(cliente.get("/api/sitios", params={"orden": "precio"}))
    assert slugs[-2:] == ["castillo-sin-precio", "zorro-sin-precio"]
    assert "cascada-veinte" in slugs[:-2]


def test_ca3_gratis_va_primero(cliente, catalogo_orden):
    """CA-3: el sitio con precio 0 va antes que los de precio mayor y antes que los sin precio."""
    slugs = _slugs(cliente.get("/api/sitios", params={"orden": "precio"}))
    assert slugs[0] == "zona-gratis"


def test_ca4_empate_por_nombre(cliente, catalogo_orden):
    """CA-4: Plaza Beta y Rio Alfa (12000) quedan por nombre, aunque Rio se insertó antes."""
    slugs = _slugs(cliente.get("/api/sitios", params={"orden": "precio"}))
    assert slugs.index("plaza-beta") + 1 == slugs.index("rio-alfa")
    assert slugs[2:4] == ["plaza-beta", "rio-alfa"]


def test_ca5_orden_predeterminado_por_nombre(cliente, catalogo_orden):
    """CA-5: sin `orden` (y con orden=nombre) la lista va por nombre normalizado, como antes."""
    esperado = [
        "cascada-veinte",
        "castillo-sin-precio",
        "laguna-quince",
        "mirador-diez",
        "plaza-beta",
        "rio-alfa",
        "zona-gratis",
        "zorro-sin-precio",
    ]
    assert _slugs(cliente.get("/api/sitios")) == esperado
    assert _slugs(cliente.get("/api/sitios", params={"orden": "nombre"})) == esperado


def test_ca6_orden_con_filtro(cliente, catalogo_orden):
    """CA-6: orden=precio y municipio=neiva: solo Neiva, en orden de precio, sin precio al final."""
    r = cliente.get("/api/sitios", params={"orden": "precio", "municipio": "neiva"})
    assert _slugs(r) == ["zona-gratis", "plaza-beta", "laguna-quince", "cascada-veinte", "zorro-sin-precio"]
    assert {s["municipio"]["clave"] for s in r.json()} == {"neiva"}


def test_ca6_orden_precio_catalogo_vacio(cliente):
    """CA-6 (límite): sin sitios, orden=precio responde 200 y lista vacía."""
    r = cliente.get("/api/sitios", params={"orden": "precio"})
    assert r.status_code == 200
    assert r.json() == []


def test_ca8_orden_invalido_422(cliente, catalogo_orden):
    """CA-8: orden=xyz da 422 con exactamente {"detalle": <texto en español>} que menciona «orden»."""
    r = cliente.get("/api/sitios", params={"orden": "xyz"})
    assert r.status_code == 422
    cuerpo = r.json()
    assert isinstance(cuerpo, dict)
    assert set(cuerpo) == {"detalle"}
    assert isinstance(cuerpo["detalle"], str) and cuerpo["detalle"]
    assert "orden" in cuerpo["detalle"].lower()
