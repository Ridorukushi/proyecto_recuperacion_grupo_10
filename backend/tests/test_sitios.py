"""Pruebas de la API de solo lectura: /api/sitios, /api/sitios/{slug} y /api/filtros.

Usan los 7 sitios semilla de datos_prueba.py (no los de backend/datos/). Orden esperado por nombre
sin tildes ni mayúsculas: Ágora, Balneario, Desierto, Malecón, Observatorio, Parque, Santuario.
"""

import pytest
from datos_prueba import ficha

SLUGS_ORDENADOS = [
    "agora-cultural-de-neiva",
    "balneario-termal-los-lagos",
    "desierto-de-la-tatacoa",
    "malecon-de-neiva",
    "observatorio-astronomico-de-la-tatacoa",
    "parque-arqueologico-de-san-agustin",
    "santuario-de-garzon",
]


def _slugs(respuesta):
    assert respuesta.status_code == 200
    return [s["slug"] for s in respuesta.json()]


def _por_slug(respuesta):
    assert respuesta.status_code == 200
    return {s["slug"]: s for s in respuesta.json()}


# ---------- Lista: CA-1, CA-3, CA-4, CA-5 ----------


def test_ca1_lista_ordenada_con_campos(cliente, catalogo_semilla):
    """CA-1: los 7 sitios, ordenados por nombre sin tildes, con nombre, municipio, categoría y precio."""
    r = cliente.get("/api/sitios")
    assert r.status_code == 200
    cuerpo = r.json()
    assert [s["slug"] for s in cuerpo] == SLUGS_ORDENADOS
    assert [(s["nombre"], s["municipio"]["etiqueta"], s["categoria"]["etiqueta"]) for s in cuerpo] == [
        ("Ágora Cultural de Neiva", "Neiva", "Cultura"),
        ("Balneario Termal Los Lagos", "Neiva", "Termales"),
        ("Desierto de la Tatacoa", "Villavieja", "Naturaleza"),
        ("Malecón de Neiva", "Neiva", "Cultura"),
        ("Observatorio Astronómico de la Tatacoa", "Villavieja", "Cultura"),
        ("Parque Arqueológico de San Agustín", "San Agustín", "Arqueología"),
        ("Santuario de Garzón", "Garzón", "Religioso"),
    ]
    assert cuerpo[2] == {
        "slug": "desierto-de-la-tatacoa",
        "nombre": "Desierto de la Tatacoa",
        "municipio": {"clave": "villavieja", "etiqueta": "Villavieja"},
        "categoria": {"clave": "naturaleza", "etiqueta": "Naturaleza"},
        "precio_referencia": {"valor_cop": 15000, "varios": True, "fecha_referencia_precio": "2026-11-24"},
    }


def test_ca1_precio_referencia_es_el_menor_conocido(cliente, catalogo_semilla):
    """CA-1: precio de referencia = menor precio conocido; varios solo si hay más de uno conocido."""
    por_slug = _por_slug(cliente.get("/api/sitios"))
    assert por_slug["parque-arqueologico-de-san-agustin"]["precio_referencia"] == {
        "valor_cop": 30000, "varios": False, "fecha_referencia_precio": "2026-11-24"}
    # Observatorio: uno conocido (12000) y uno desconocido descartado -> no es "varios".
    assert por_slug["observatorio-astronomico-de-la-tatacoa"]["precio_referencia"] == {
        "valor_cop": 12000, "varios": False, "fecha_referencia_precio": "2026-10-15"}


def test_ca3_precio_desconocido_es_null(cliente, catalogo_semilla):
    """CA-3: sin precio conocido el campo es null (nunca 0), también si el único precio era desconocido."""
    por_slug = _por_slug(cliente.get("/api/sitios"))
    for slug in ("balneario-termal-los-lagos", "agora-cultural-de-neiva"):
        assert "precio_referencia" in por_slug[slug]
        assert por_slug[slug]["precio_referencia"] is None


def test_ca4_precio_cero_no_es_null(cliente, catalogo_semilla):
    """CA-4: precio 0 es gratis (valor_cop 0), distinto de desconocido (null)."""
    por_slug = _por_slug(cliente.get("/api/sitios"))
    assert por_slug["malecon-de-neiva"]["precio_referencia"] == {
        "valor_cop": 0, "varios": False, "fecha_referencia_precio": "2026-11-24"}
    # Gratis con otras tarifas: el menor es 0 y hay varios.
    assert por_slug["santuario-de-garzon"]["precio_referencia"] == {
        "valor_cop": 0, "varios": True, "fecha_referencia_precio": "2026-11-24"}


def test_ca5_catalogo_vacio(cliente):
    """CA-5: sin sitios la API responde 200 con una lista vacía."""
    r = cliente.get("/api/sitios")
    assert r.status_code == 200
    assert r.json() == []


# ---------- Ficha: CA-6, CA-8, CA-9, CA-20 ----------


def test_ca6_ficha_completa(cliente, catalogo_semilla):
    """CA-6: la ficha trae todos los campos, cada precio con su concepto y las fuentes."""
    r = cliente.get("/api/sitios/desierto-de-la-tatacoa")
    assert r.status_code == 200
    cuerpo = r.json()
    precios = sorted(cuerpo.pop("precios"), key=lambda p: p["concepto"])
    fuentes = sorted(cuerpo.pop("fuentes"))
    assert precios == [
        {"concepto": "Entrada adulto", "valor_cop": 25000},
        {"concepto": "Entrada niño", "valor_cop": 15000},
    ]
    assert fuentes == ["https://example.org/tatacoa-a", "https://example.org/tatacoa-b"]
    assert cuerpo == {
        "slug": "desierto-de-la-tatacoa",
        "nombre": "Desierto de la Tatacoa",
        "municipio": {"clave": "villavieja", "etiqueta": "Villavieja"},
        "categoria": {"clave": "naturaleza", "etiqueta": "Naturaleza"},
        "descripcion": "Zona árida de prueba con cielos despejados.",
        "latitud": 3.2333,
        "longitud": -75.1667,
        "horario": "Todos los días, 24 horas",
        "como_llegar": "Desde Neiva por la vía a Villavieja.",
        "fecha_referencia_precio": "2026-11-24",
    }


def test_ca6_ficha_gratis_conserva_el_cero(cliente, catalogo_semilla):
    """CA-4/CA-6 (límite): en la ficha el precio 0 aparece como 0, no se pierde ni pasa a null."""
    cuerpo = cliente.get("/api/sitios/malecon-de-neiva").json()
    assert cuerpo["precios"] == [{"concepto": "Entrada", "valor_cop": 0}]


def test_ca8_campos_desconocidos_null(cliente, catalogo_semilla):
    """CA-8: horario, cómo llegar, descripción y fecha desconocidos llegan como null; sin precios, lista vacía."""
    r = cliente.get("/api/sitios/balneario-termal-los-lagos")
    assert r.status_code == 200
    cuerpo = r.json()
    for campo in ("horario", "como_llegar", "descripcion", "fecha_referencia_precio"):
        assert campo in cuerpo
        assert cuerpo[campo] is None
    assert cuerpo["precios"] == []
    assert cuerpo["fuentes"] == ["https://example.org/balneario"]


def test_ca8_precios_desconocidos_no_aparecen(cliente, catalogo_semilla):
    """CA-8: solo se muestran los precios conocidos (el desconocido se descarta)."""
    cuerpo = cliente.get("/api/sitios/observatorio-astronomico-de-la-tatacoa").json()
    assert cuerpo["precios"] == [{"concepto": "Entrada", "valor_cop": 12000}]
    assert cliente.get("/api/sitios/agora-cultural-de-neiva").json()["precios"] == []


def test_ca9_slug_inexistente_404(cliente, catalogo_semilla):
    """CA-9: un slug que no existe responde 404 con «Sitio no encontrado.»."""
    r = cliente.get("/api/sitios/sitio-que-no-existe")
    assert r.status_code == 404
    assert r.json() == {"detalle": "Sitio no encontrado."}


@pytest.mark.parametrize(
    "slug_invalido",
    ["Desierto-De-La-Tatacoa", "desierto_de_la_tatacoa", "a" * 121, "x'--"],
)
def test_ca9_slug_invalido_404(cliente, catalogo_semilla, slug_invalido):
    """CA-9: un slug con formato inválido responde 404 igual que uno inexistente."""
    r = cliente.get(f"/api/sitios/{slug_invalido}")
    assert r.status_code == 404
    assert r.json() == {"detalle": "Sitio no encontrado."}


def test_ca20_ficha_por_slug(cliente, catalogo_semilla):
    """CA-20: el sitio «Desierto de la Tatacoa» se abre por /desierto-de-la-tatacoa y es el mismo de la lista."""
    r = cliente.get("/api/sitios/desierto-de-la-tatacoa")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Desierto de la Tatacoa"
    assert r.json()["slug"] == "desierto-de-la-tatacoa"
    assert "desierto-de-la-tatacoa" in _slugs(cliente.get("/api/sitios"))


# ---------- Filtros: CA-10 a CA-13 y CA-15 ----------


def test_ca10_filtra_por_municipio(cliente, catalogo_semilla):
    """CA-10: solo los sitios del municipio elegido, en orden alfabético."""
    r = cliente.get("/api/sitios", params={"municipio": "neiva"})
    assert _slugs(r) == ["agora-cultural-de-neiva", "balneario-termal-los-lagos", "malecon-de-neiva"]
    assert {s["municipio"]["clave"] for s in r.json()} == {"neiva"}


def test_ca10_municipio_valido_sin_sitios_es_lista_vacia(cliente, catalogo_semilla):
    """CA-10 (límite): un municipio que existe pero no tiene sitios devuelve 200 y lista vacía."""
    r = cliente.get("/api/sitios", params={"municipio": "pitalito"})
    assert r.status_code == 200
    assert r.json() == []


def test_ca11_filtra_por_categoria(cliente, catalogo_semilla):
    """CA-11: solo los sitios de la categoría elegida."""
    r = cliente.get("/api/sitios", params={"categoria": "cultura"})
    assert _slugs(r) == [
        "agora-cultural-de-neiva", "malecon-de-neiva", "observatorio-astronomico-de-la-tatacoa"]
    assert {s["categoria"]["clave"] for s in r.json()} == {"cultura"}
    r = cliente.get("/api/sitios", params={"categoria": "arqueologia"})
    assert _slugs(r) == ["parque-arqueologico-de-san-agustin"]


@pytest.mark.parametrize("q", ["tatacoa", "TATACOA", "TaTaCoA", "  tatacoa  "])
def test_ca12_busca_sin_tildes_ni_mayusculas(cliente, catalogo_semilla, q):
    """CA-12: «tatacoa» y «TATACOA» encuentran los mismos sitios."""
    r = cliente.get("/api/sitios", params={"q": q})
    assert _slugs(r) == ["desierto-de-la-tatacoa", "observatorio-astronomico-de-la-tatacoa"]


@pytest.mark.parametrize(
    ("q", "esperado"),
    [
        ("malecon", ["malecon-de-neiva"]),  # sin tilde encuentra «Malecón»
        ("MALECÓN", ["malecon-de-neiva"]),  # con tilde y mayúsculas también
        ("astronomico", ["observatorio-astronomico-de-la-tatacoa"]),
        ("Agustín", ["parque-arqueologico-de-san-agustin"]),
        ("agora", ["agora-cultural-de-neiva"]),
        ("no-existe-este-nombre", []),
    ],
)
def test_ca12_busca_por_parte_del_nombre(cliente, catalogo_semilla, q, esperado):
    """CA-12: coincide con parte del nombre, sin importar tildes ni mayúsculas; sin coincidencias, lista vacía."""
    assert _slugs(cliente.get("/api/sitios", params={"q": q})) == esperado


def test_ca12_comodines_literales(cargar, cliente):
    """CA-12: «%» y «_» en la búsqueda son texto literal, no comodines de SQL."""
    cargar([
        ficha(nombre="Ruta 100% Café"),
        ficha(nombre="Ruta 1000 Café"),
        ficha(nombre="Finca Los_Pinos"),
        ficha(nombre="Finca LosXPinos"),
    ])
    por_porcentaje = [s["nombre"] for s in cliente.get("/api/sitios", params={"q": "100%"}).json()]
    assert por_porcentaje == ["Ruta 100% Café"]
    por_guion = [s["nombre"] for s in cliente.get("/api/sitios", params={"q": "los_pinos"}).json()]
    assert por_guion == ["Finca Los_Pinos"]
    assert [s["nombre"] for s in cliente.get("/api/sitios", params={"q": "%"}).json()] == ["Ruta 100% Café"]


@pytest.mark.parametrize("q", ["", "   "])
def test_ca12_busqueda_vacia(cliente, catalogo_semilla, q):
    """CA-12 (límite): búsqueda vacía o solo con espacios = sin búsqueda: se devuelven todos."""
    assert _slugs(cliente.get("/api/sitios", params={"q": q})) == SLUGS_ORDENADOS


def test_ca12_busqueda_de_100_caracteres_es_valida(cliente, catalogo_semilla):
    """CA-12/CA-15 (límite): 100 caracteres es el máximo permitido."""
    r = cliente.get("/api/sitios", params={"q": "a" * 100})
    assert r.status_code == 200
    assert r.json() == []


def test_ca13_filtros_combinados(cliente, catalogo_semilla):
    """CA-13: municipio, categoría y texto a la vez: solo quedan los que cumplen los tres."""
    r = cliente.get("/api/sitios", params={"municipio": "villavieja", "categoria": "cultura", "q": "tatacoa"})
    assert _slugs(r) == ["observatorio-astronomico-de-la-tatacoa"]
    r = cliente.get("/api/sitios", params={"municipio": "neiva", "categoria": "cultura", "q": "de"})
    assert _slugs(r) == ["agora-cultural-de-neiva", "malecon-de-neiva"]
    r = cliente.get("/api/sitios", params={"municipio": "villavieja", "categoria": "naturaleza"})
    assert _slugs(r) == ["desierto-de-la-tatacoa"]


def test_ca13_combinacion_sin_resultados(cliente, catalogo_semilla):
    """CA-13/CA-14: una combinación válida sin coincidencias da 200 y lista vacía."""
    r = cliente.get("/api/sitios", params={"municipio": "neiva", "categoria": "cultura", "q": "tatacoa"})
    assert r.status_code == 200
    assert r.json() == []


def _es_error_claro(respuesta, *fragmentos):
    assert respuesta.status_code == 422
    cuerpo = respuesta.json()
    assert isinstance(cuerpo, dict)
    assert set(cuerpo) == {"detalle"}, "el error solo debe traer «detalle» (sin loc, trazas ni SQL)"
    assert isinstance(cuerpo["detalle"], str) and cuerpo["detalle"]
    for fragmento in fragmentos:
        assert fragmento.lower() in cuerpo["detalle"].lower()


def test_ca15_municipio_invalido_422(cliente, catalogo_semilla):
    """CA-15: un municipio que no existe da 422 con mensaje en español, no una lista vacía."""
    _es_error_claro(cliente.get("/api/sitios", params={"municipio": "xyz"}), "municipio", "xyz")


def test_ca15_categoria_invalida_422(cliente, catalogo_semilla):
    """CA-15: una categoría que no existe da 422 con mensaje en español."""
    _es_error_claro(cliente.get("/api/sitios", params={"categoria": "deportes"}), "categoria")


def test_ca15_busqueda_larga_422(cliente, catalogo_semilla):
    """CA-15: una búsqueda de más de 100 caracteres da 422 con mensaje claro."""
    _es_error_claro(cliente.get("/api/sitios", params={"q": "a" * 101}), "100")


# ---------- /api/filtros ----------


def test_filtros_lista_municipios_y_categorias(cliente, catalogo_semilla):
    """GET /api/filtros: municipios cargados y las 7 categorías, ordenados por etiqueta."""
    r = cliente.get("/api/filtros")
    assert r.status_code == 200
    assert r.json() == {
        "municipios": [
            {"clave": "garzon", "etiqueta": "Garzón"},
            {"clave": "neiva", "etiqueta": "Neiva"},
            {"clave": "pitalito", "etiqueta": "Pitalito"},
            {"clave": "san-agustin", "etiqueta": "San Agustín"},
            {"clave": "villavieja", "etiqueta": "Villavieja"},
        ],
        "categorias": [
            {"clave": "arqueologia", "etiqueta": "Arqueología"},
            {"clave": "aventura", "etiqueta": "Aventura"},
            {"clave": "cultura", "etiqueta": "Cultura"},
            {"clave": "gastronomia", "etiqueta": "Gastronomía"},
            {"clave": "naturaleza", "etiqueta": "Naturaleza"},
            {"clave": "religioso", "etiqueta": "Religioso"},
            {"clave": "termales", "etiqueta": "Termales"},
        ],
    }


# ---------- RF-012: solo lectura ----------


@pytest.mark.parametrize("metodo", ["post", "put", "delete", "patch"])
def test_rf012_catalogo_de_solo_lectura(cliente, catalogo_semilla, metodo):
    """RF-012: no hay creación, edición ni borrado desde la API."""
    r = getattr(cliente, metodo)("/api/sitios/desierto-de-la-tatacoa")
    assert r.status_code == 405
    assert cliente.get("/api/sitios/desierto-de-la-tatacoa").status_code == 200
