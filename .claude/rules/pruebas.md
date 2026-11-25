---
paths:
  - "backend/tests/**"
  - "frontend/src/**/*.spec.ts"
---

# Reglas de las pruebas

- Backend: pytest en `backend/tests/test_<modulo>.py`, con el `TestClient` de FastAPI. Frontend: vitest en `*.spec.ts` junto al componente o servicio.
- Cada prueba cita el criterio de aceptación que verifica en su nombre o docstring, por ejemplo `test_ca3_filtra_por_municipio`.
- El resultado esperado se deduce del criterio de aceptación, nunca de lo que devuelve el código.
- Cada prueba tiene al menos una aserción concreta. Prohibido: `pytest.mark.skip`, `it.skip`, `it.only` y pruebas que solo verifican que «no lanza error».
- Siempre se incluyen el caso límite (lista vacía, precio 0, borde del Huila) y el caso de error (dato inválido → 422 o mensaje claro).
- Ninguna prueba llama a la API real de Claude ni a internet: se usan dobles de prueba. La base de datos de pruebas es independiente de la de desarrollo.
- Las pruebas se escriben antes del código (Red), se confirma que fallan por el motivo esperado y se suben en su propio commit.
