"""Pruebas de app.texto: normalizar() y slug() (CA-12 y CA-20)."""

import pytest


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("TATACOA", "tatacoa"),
        ("Tatacoa", "tatacoa"),
        ("Malecón", "malecon"),
        ("ÁÉÍÓÚ áéíóú", "aeiou aeiou"),
        ("Ñame", "name"),  # D5: la ñ pasa a n
        ("Desierto   de  la\tTatacoa", "desierto de la tatacoa"),
        ("  Café  ", "cafe"),
        ("", ""),
    ],
)
def test_ca12_normalizar(entrada, esperado):
    """CA-12: normalizar quita tildes, pasa a minúsculas y colapsa espacios."""
    from app.texto import normalizar

    assert normalizar(entrada) == esperado


@pytest.mark.parametrize(
    ("nombre", "esperado"),
    [
        ("Desierto de la Tatacoa", "desierto-de-la-tatacoa"),
        ("Parque Arqueológico de San Agustín", "parque-arqueologico-de-san-agustin"),
        ("Cañón del Río", "canon-del-rio"),
        ("  Café & Té: 100% Huila!! ", "cafe-te-100-huila"),
        ("---A--B---", "a-b"),
    ],
)
def test_ca20_slug(nombre, esperado):
    """CA-20: el slug es minúsculas, sin tildes, con guiones y sin guiones en los extremos."""
    from app.texto import slug

    assert slug(nombre) == esperado
