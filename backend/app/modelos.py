"""Tablas SQLAlchemy (el esquema real vive en backend/db/001_esquema.sql)."""

from datetime import date

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Municipio(Base):
    __tablename__ = "municipio"

    clave: Mapped[str] = mapped_column(primary_key=True)
    nombre: Mapped[str]


class Sitio(Base):
    __tablename__ = "sitio"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str]
    nombre: Mapped[str]
    nombre_normalizado: Mapped[str]
    municipio_clave: Mapped[str] = mapped_column(ForeignKey("municipio.clave"))
    categoria: Mapped[str]
    descripcion: Mapped[str | None]
    latitud: Mapped[float] = mapped_column(Numeric(8, 5, asdecimal=False))
    longitud: Mapped[float] = mapped_column(Numeric(8, 5, asdecimal=False))
    horario: Mapped[str | None]
    como_llegar: Mapped[str | None]
    fecha_referencia_precio: Mapped[date | None]

    municipio: Mapped[Municipio] = relationship()
    precios: Mapped[list["Precio"]] = relationship(order_by="Precio.id")
    fuentes: Mapped[list["Fuente"]] = relationship(order_by="Fuente.id")


class Precio(Base):
    __tablename__ = "precio"

    id: Mapped[int] = mapped_column(primary_key=True)
    sitio_id: Mapped[int] = mapped_column(ForeignKey("sitio.id"))
    concepto: Mapped[str]
    valor_cop: Mapped[int]


class Fuente(Base):
    __tablename__ = "fuente"

    id: Mapped[int] = mapped_column(primary_key=True)
    sitio_id: Mapped[int] = mapped_column(ForeignKey("sitio.id"))
    url: Mapped[str]
