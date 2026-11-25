---
description: "Tareas de la spec 002-ordenar-por-precio"
---

# Tareas: Ordenar la lista de sitios por precio

**Entrada**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md),
[contracts/openapi-cambios.yaml](contracts/openapi-cambios.yaml), [quickstart.md](quickstart.md).

**Pruebas**: obligatorias (constitución III y IV). Se escriben primero (Red) y se suben en un commit `test:` antes del
código.

**Historias**: US1 = ver primero los sitios más económicos (P1); US2 = elegir el orden y combinarlo con los filtros (P1).

**Formato**: `- [ ] Tnnn [P?] [US?] descripción con ruta`. `[P]` = paralelizable (archivo distinto, sin dependencias).

---

## Fase 1: Preparación

- [ ] T001 Confirmar que las suites actuales están en verde antes de empezar (`cd backend && uv run pytest -q`, `cd frontend && npx ng test --watch=false`)

---

## Fase 2: Red (pruebas primero)

- [ ] T002 [P] [US1] Crear `backend/tests/test_orden.py` con CA-1, CA-2, CA-3 y CA-4 sobre `GET /api/sitios?orden=precio`, usando sitios semilla propios con precios 20.000, 10.000, 15.000, 0, un empate y dos sin precio (regla de `data-model.md`, sección «Regla de orden por precio»)
- [ ] T003 [US2] Agregar a `backend/tests/test_orden.py` CA-5 (sin `orden` = por nombre), CA-6 (`orden=precio` con `municipio`) y CA-8 (`orden=xyz` → 422 con `{"detalle": …}` en español)
- [ ] T004 [P] [US2] Agregar a `frontend/src/app/services/sitios.service.spec.ts` la prueba CA-7: `listar({orden: 'precio'})` envía `orden=precio` y `listar({orden: 'nombre'})` no envía el parámetro
- [ ] T005 [P] [US2] Agregar a `frontend/src/app/pages/lista-sitios/lista-sitios.spec.ts` CA-5 (selector con etiqueta visible «Ordenar por» y «Nombre (A–Z)» elegido; RF-008), CA-6 y CA-7 (elegir precio pide `orden=precio`; abrir con `?orden=precio` en la URL lo respeta) y CA-9 («Limpiar filtros» vuelve a nombre)
- [ ] T006 Ejecutar ambas suites, comprobar que las pruebas nuevas fallan por falta de código y hacer commit `test:` solo con las pruebas

**Punto de control**: CA-1 a CA-9 tienen prueba y están en rojo.

---

## Fase 3: Green (implementación con `/speckit-implement`)

### US1: Orden por precio en la API
- [ ] T007 [US1] En `backend/app/rutas/sitios.py`, agregar el parámetro `orden` (`nombre` por defecto) y, con `orden=precio`, ordenar la lista ya filtrada por la clave de `data-model.md` («Regla de orden por precio»: sin precio al final, `precio_referencia.valor_cop`, `sitio.nombre_normalizado`) — CA-1 a CA-4, CA-6

### US2: Validación y selector
- [ ] T008 [US2] En `backend/app/rutas/sitios.py`, rechazar un `orden` fuera de los valores de `data-model.md` `orden` con 422 y el mensaje de `research.md` D2 — CA-8
- [ ] T009 [P] [US2] En `frontend/src/app/services/sitios.service.ts`, agregar `orden` a los filtros y enviarlo solo cuando es `precio` — CA-7
- [ ] T010 [US2] En `frontend/src/app/pages/lista-sitios/lista-sitios.ts` y `.html`, agregar el signal `orden`, el `<select id="orden">` con etiqueta «Ordenar por», leerlo y escribirlo en la URL y reiniciarlo en «Limpiar filtros» (`research.md` D3) — CA-5, CA-6, CA-7, CA-9

- [ ] T011 Ejecutar ambas suites, `uv run ruff check` y `npm run build` en verde y hacer commit `feat:`

---

## Fase 4: Verificación

- [ ] T012 Ejecutar `/speckit-converge` para comparar el código con la spec, el plan y estas tareas
- [ ] T013 Recorrer los escenarios de `quickstart.md` con el catálogo real

---

## Fase 5: Cierre

- [ ] T014 Marcar `[X]` las tareas con evidencia y subir los commits a la rama

---

## Dependencias
- T001 → Red (T002–T006) → Green (T007–T011) → Verificación → Cierre.
- T007 antes de T008 (mismo archivo). T009 antes de T010 (la pantalla usa el servicio).

## Paralelo
- Red: T002, T004 y T005 tocan archivos distintos.
- Green: T009 puede hacerse junto con T007/T008 (backend y frontend separados).

## Estrategia
- MVP: US1 (orden por precio en la API). US2 completa la funcionalidad en la pantalla.
