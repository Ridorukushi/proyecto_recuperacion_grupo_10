"""Normalización de texto para búsqueda, orden y slugs (research D5 y D6)."""

import re
import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes (NFD sin marcas) y con los espacios colapsados."""
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_marcas = "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")
    return " ".join(sin_marcas.lower().split())


def slug(nombre: str) -> str:
    """Identificador legible: a-z, 0-9 y guiones, sin guiones en los extremos."""
    return re.sub(r"[^a-z0-9]+", "-", normalizar(nombre)).strip("-")
