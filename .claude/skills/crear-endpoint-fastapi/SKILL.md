---
name: crear-endpoint-fastapi
description: Procedimiento para crear o cambiar un endpoint del backend FastAPI de Turismo Huila - contrato Pydantic, validación, consulta a PostgreSQL, errores en español y prueba. Úsala al tocar backend/app/.
---

# Crear un endpoint en FastAPI

1. **Contrato primero.** Copia del `plan.md` la ruta, el método, los parámetros y la respuesta. Si el
   contrato no está en el plan, detente: hay que actualizar el plan antes.
2. **Esquemas.** Define los modelos Pydantic de entrada y salida en el módulo de esquemas del recurso.
   Aplica las reglas de la skill `datos-turisticos` (rangos de coordenadas, precios ≥ 0, listas permitidas)
   con `Field(...)` y validadores, no con `if` sueltos en el endpoint.
3. **Acceso a datos.** La consulta vive en una función de repositorio/servicio, separada del endpoint, con
   parámetros (nunca concatenando texto del usuario). Paginación con límite máximo.
4. **Endpoint.** Recibe dependencias con `Depends` (sesión de base de datos, configuración). Declara
   `response_model`. Devuelve 404 o 422 con mensajes en español y sin detalles internos.
5. **Registro.** Incluye el router en la aplicación y verifica que aparece en `/docs` (OpenAPI).
6. **Configuración.** Cada variable de entorno nueva va a la configuración central y a `.env.example` sin valor.
7. **Prueba.** Las pruebas ya las escribió el `probador`; ejecútalas hasta que pasen sin modificarlas.
