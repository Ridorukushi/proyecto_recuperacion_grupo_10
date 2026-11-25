"""CA-16 sobre los archivos reales de backend/datos/ (catálogo inicial y municipios)."""

import json
from pathlib import Path

DATOS = Path(__file__).resolve().parent.parent / "datos"
RUTA_SITIOS = DATOS / "sitios.json"
RUTA_MUNICIPIOS = DATOS / "municipios.json"


def _leer(ruta: Path):
    assert ruta.is_file(), f"Falta el archivo {ruta.name} en backend/datos/"
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_ca16_catalogo_inicial_valido():
    """CA-16: 10 a 15 fichas válidas, con fuente y coordenadas, nombres únicos y con la Tatacoa."""
    from app.esquemas import FichaSitio
    from app.texto import slug

    fichas = _leer(RUTA_SITIOS)
    assert 10 <= len(fichas) <= 15

    claves_municipio = {m["clave"] for m in _leer(RUTA_MUNICIPIOS)["municipios"]}
    modelos = [FichaSitio.model_validate(f) for f in fichas]  # valida todas las reglas de datos

    for f in fichas:
        assert f["nombre"].strip(), "ficha sin nombre"
        assert f["municipio"] in claves_municipio, f"{f['nombre']}: municipio fuera del Huila"
        assert f["categoria"], f"{f['nombre']}: sin categoría"
        assert f["latitud"] is not None and f["longitud"] is not None
        assert 1.5 <= f["latitud"] <= 3.9, f"{f['nombre']}: latitud fuera del Huila"
        assert -76.6 <= f["longitud"] <= -74.4, f"{f['nombre']}: longitud fuera del Huila"
        assert len(f["fuentes"]) >= 1, f"{f['nombre']}: sin fuente"
        assert all(u.startswith(("http://", "https://")) for u in f["fuentes"])

    nombres = [f["nombre"] for f in fichas]
    slugs = [slug(n) for n in nombres]
    assert len(set(nombres)) == len(nombres)
    assert len(set(slugs)) == len(slugs)
    assert "desierto-de-la-tatacoa" in slugs
    assert len(modelos) == len(fichas)


def test_ca16_municipios_del_huila():
    """CA-16: 37 municipios con clave y nombre únicos, y una fuente."""
    datos = _leer(RUTA_MUNICIPIOS)
    assert datos["fuente"].startswith(("http://", "https://"))
    municipios = datos["municipios"]
    assert len(municipios) == 37
    claves = [m["clave"] for m in municipios]
    nombres = [m["nombre"] for m in municipios]
    assert len(set(claves)) == 37
    assert len(set(nombres)) == 37
    assert all(c == c.lower() and " " not in c for c in claves)
    assert {"neiva", "garzon", "villavieja", "san-agustin", "la-plata"} <= set(claves)


def test_ca16_catalogo_real_se_carga_completo(sesion, contar):
    """CA-16: los archivos reales pasan cargar_catalogo y quedan guardados."""
    from app.carga import cargar_catalogo

    cargar_catalogo(sesion, RUTA_SITIOS, RUTA_MUNICIPIOS)
    sesion.commit()
    assert contar("municipio") == 37
    assert 10 <= contar("sitio") <= 15
    assert contar("fuente") >= contar("sitio")
