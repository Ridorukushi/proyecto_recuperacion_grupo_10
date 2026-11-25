---
paths:
  - "backend/app/**"
---

# Reglas del backend (FastAPI)

- Cada endpoint declara su modelo de entrada y de respuesta con Pydantic. Lo que no está en el contrato del `plan.md` no se expone.
- Toda entrada se valida en el servidor: coordenadas dentro del Huila, precios enteros ≥ 0, municipio y categoría de la lista permitida (skill `datos-turisticos`).
- Consultas a PostgreSQL siempre parametrizadas (ORM o parámetros), nunca concatenando texto del usuario.
- La configuración (URL de la base de datos, llave de la API de Claude) se lee de variables de entorno. Cada variable nueva se agrega a `.env.example` sin valor real.
- Errores: 404 si el sitio no existe, 422 si la entrada es inválida, y mensajes en español sin detalles internos (sin trazas ni SQL).
- La llamada a la API de Claude vive en un único módulo del backend, con tiempo límite y manejo de error. El prompt le entrega solo datos del catálogo.
