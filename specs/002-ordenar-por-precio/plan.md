# Plan de implementación: Ordenar la lista de sitios por precio

**Rama**: `feat/002-ordenar-por-precio` | **Fecha**: 2026-11-25 | **Spec**: [spec.md](spec.md)

**Entrada**: spec aprobada en `specs/002-ordenar-por-precio/spec.md`.

**Estado**: Aprobado (2026-11-25).

## Resumen
Se agrega el parámetro `orden` (`nombre` | `precio`) a `GET /api/sitios`. El backend ordena por precio de
referencia en memoria, con los sitios sin precio al final. En el frontend, la pantalla de lista suma un selector
«Ordenar por», que se guarda en la URL y se reinicia con «Limpiar filtros». Detalle en [research.md](research.md),
[data-model.md](data-model.md), [contracts/openapi-cambios.yaml](contracts/openapi-cambios.yaml) y
[quickstart.md](quickstart.md).

## Contexto técnico
**Lenguaje/versión**: Python 3.12 (backend); TypeScript con Angular 21 (frontend). Igual que la spec 001.

**Dependencias principales**: las de la spec 001; ninguna nueva.

**Almacenamiento**: PostgreSQL 16, sin cambios de esquema.

**Pruebas**: pytest (`cd backend && uv run pytest -q`) y vitest (`cd frontend && npx ng test --watch=false`).

**Tipo de proyecto**: aplicación web (`backend/` y `frontend/`).

**Escala**: 10 a 15 sitios; ordenar en memoria es suficiente.

## Constitution Check
| Principio | Cómo lo cumple | Estado |
|---|---|---|
| I. Specs | Spec aprobada; plan con aprobación antes de código. | ✅ |
| II. Datos verificables | Un sitio sin precio nunca se ordena como gratis (RF-002). No hay datos nuevos. | ✅ |
| III. Pruebas y contratos | Cambio de contrato en `contracts/` antes del código; pruebas primero. | ✅ |
| IV. Trazabilidad | Commits por paso del flujo (`test:` antes de `feat:`). | ✅ |
| V. Seguridad y simplicidad | `orden` validado en el servidor con lista cerrada; sin dependencias; orden en memoria (YAGNI). | ✅ |

Sin violaciones. Sin excepciones que justificar.

## Estructura (archivos que se tocan)
```text
backend/app/repositorio.py        # listar_sitios: sin cambios en la consulta
backend/app/rutas/sitios.py       # parámetro orden, validación 422, orden por precio
backend/tests/test_orden.py       # NUEVO: CA-1 a CA-4 y CA-8 (API)
frontend/src/app/services/sitios.service.ts        # envía orden=precio
frontend/src/app/services/sitios.service.spec.ts   # CA-7 (parámetro)
frontend/src/app/pages/lista-sitios/lista-sitios.{ts,html}   # selector «Ordenar por»
frontend/src/app/pages/lista-sitios/lista-sitios.spec.ts     # CA-5, CA-6, CA-9
```

## Criterio → prueba
| CA | Qué se verifica | Prueba |
|---|---|---|
| CA-1 | Precios 20.000, 10.000 y 15.000 quedan en orden 10.000, 15.000, 20.000 | `test_orden.py::test_ca1_ordena_por_precio_de_menor_a_mayor` |
| CA-2 | Sin precio al final, ordenados por nombre | `test_orden.py::test_ca2_sin_precio_al_final_por_nombre` |
| CA-3 | Gratis (0) antes que precios mayores y que sin precio | `test_orden.py::test_ca3_gratis_va_primero` |
| CA-4 | Empate de precio se resuelve por nombre | `test_orden.py::test_ca4_empate_por_nombre` |
| CA-5 | Sin `orden` se ordena por nombre; el selector muestra «Nombre (A–Z)» | `test_orden.py::test_ca5_orden_predeterminado_por_nombre`; `lista-sitios.spec.ts` «CA-5 (spec 002) …» |
| CA-6 | Orden por precio combinado con filtro de municipio | `test_orden.py::test_ca6_orden_con_filtro`; `lista-sitios.spec.ts` «CA-6 (spec 002) …» |
| CA-7 | El servicio envía `orden=precio` y la pantalla lo lee de la URL | `sitios.service.spec.ts` «CA-7 (spec 002) …»; `lista-sitios.spec.ts` «CA-7 (spec 002) …» |
| CA-8 | `orden=xyz` → 422 en español | `test_orden.py::test_ca8_orden_invalido_422` |
| CA-9 | «Limpiar filtros» vuelve a nombre | `lista-sitios.spec.ts` «CA-9 (spec 002) …» |
