---
name: escribir-pruebas
description: Cómo escribir pruebas a partir de criterios de aceptación en este proyecto - pytest con TestClient de FastAPI en el backend y vitest en Angular. Úsala en la fase Red o al revisar si una prueba realmente verifica algo.
---

# Escribir pruebas desde la spec

## Proceso
1. Lista los criterios de aceptación (CA-n) de `spec.md` y, para cada uno, escribe en una línea:
   *dado / cuando / entonces* con valores concretos.
2. Calcula a mano el resultado esperado. Si no puedes deducirlo de la spec, la spec está incompleta:
   pregúntalo, no lo adivines.
3. Escribe una prueba por criterio más el caso límite y el caso de error.
4. Ejecuta y confirma que falla por el motivo esperado (Red).

## Backend (pytest + FastAPI)
- Archivo: `backend/tests/test_<recurso>.py`. Nombre: `test_ca<n>_<comportamiento>`.
- Usa el `TestClient` de FastAPI y fixtures de `conftest.py` para la base de datos de prueba y los datos semilla.
- Verifica código HTTP **y** contenido: no basta con `status_code == 200`.
- Casos típicos de este proyecto: filtro que no devuelve nada (lista vacía, 200), municipio inexistente (422),
  sitio inexistente (404), precio ausente (campo `null`, no `0`), coordenadas en el borde del Huila.
- La API de Claude se reemplaza con un doble de prueba (`monkeypatch` o inyección de dependencias de FastAPI).

## Frontend (vitest + Angular)
- Archivo `*.spec.ts` junto al componente o servicio. Nombres de `describe`/`it` en español.
- Servicios: `provideHttpClientTesting` y `HttpTestingController` para simular respuestas del backend.
- Componentes: verifica lo que ve el usuario (texto, estados de carga/vacío/error), no detalles internos.
- Formato de precio: «$25.000 COP (aprox., …)» y «Precio no disponible» cuando no hay precio.

## Señales de una mala prueba
Sin aserción, que repite la lógica del código para calcular lo esperado, que solo verifica un mock,
que pasa antes de existir el código, o con `skip`/`only`.
