"""Configuración desde variables de entorno o backend/.env (nunca valores en el código)."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

RAIZ_BACKEND = Path(__file__).resolve().parent.parent


class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(env_file=RAIZ_BACKEND / ".env", extra="ignore")

    database_url: str = ""
    origenes_permitidos: str = ""

    @property
    def origenes(self) -> list[str]:
        return [o.strip() for o in self.origenes_permitidos.split(",") if o.strip()]


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()
