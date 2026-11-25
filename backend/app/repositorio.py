"""Consultas a la base (siempre parametrizadas)."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.modelos import Municipio, Sitio
from app.texto import normalizar


def _escapar_like(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _consulta_base():
    return select(Sitio).options(
        joinedload(Sitio.municipio),
        selectinload(Sitio.precios),
        selectinload(Sitio.fuentes),
    )


def listar_sitios(
    sesion: Session, municipio: str | None, categoria: str | None, q: str | None
) -> list[Sitio]:
    consulta = _consulta_base()
    if municipio:
        consulta = consulta.where(Sitio.municipio_clave == municipio)
    if categoria:
        consulta = consulta.where(Sitio.categoria == categoria)
    texto = normalizar(q or "")
    if texto:
        consulta = consulta.where(Sitio.nombre_normalizado.like(f"%{_escapar_like(texto)}%", escape="\\"))
    # COLLATE "C": el orden no depende de la configuración regional del servidor (research D5).
    consulta = consulta.order_by(Sitio.nombre_normalizado.collate("C"))
    return list(sesion.scalars(consulta))


def obtener_sitio(sesion: Session, slug: str) -> Sitio | None:
    return sesion.scalars(_consulta_base().where(Sitio.slug == slug)).first()


def listar_municipios(sesion: Session) -> list[Municipio]:
    return list(sesion.scalars(select(Municipio)))
