# 001-catalogo-sitios: evidencia de calidad

## Historial (las pruebas van antes del código)
| Commit | Qué es |
|---|---|
| `bc130c7` | Spec aprobada (prompt, spec y checklist). |
| `2bb1230` | Plan aprobado (contrato OpenAPI, modelo de datos y criterio → prueba). |
| `7ae0973` | Tareas y ajustes de `/speckit-analyze`. |
| `4527c45` | Preparación: backend, Angular 21, PostgreSQL en el CI y comandos oficiales. |
| `a35851d` | Datos: 37 municipios y 10 sitios con fuentes (`curador-datos`). |
| `1776bc4` | **Red:** 91 casos pytest y 35 `it` de vitest, sin código. |
| `…` | **Green:** implementación. |
| `…` | Arreglos tras la revisión. |

## Evidencia del Red
Ejecutado por el orquestador el 2026-11-24, después del informe del `probador`.

**Backend:** `cd backend && uv run pytest -q --tb=no`
```text
14 failed, 1 passed, 76 errors in 0.61s
```
- Los 90 fallos y errores son `ModuleNotFoundError: No module named 'app'`: el paquete `app` todavía no existe.
  Los 76 «errors» ocurren al preparar la fixture `motor`, que importa `app.db`. Ninguna falla viene de un error
  de sintaxis de las pruebas.
- Pasa 1: `test_datos.py::test_ca16_municipios_del_huila`, porque solo valida el archivo de datos
  `backend/datos/municipios.json`, que ya está en el commit `a35851d`. Es una prueba de datos, no de código, y es
  correcto que pase.

**Frontend:** `cd frontend && npx ng test --watch=false`
```text
Application bundle generation failed
TS2307: Cannot find module './precio' | './mapa' | './sitios.service' | './lista-sitios' | './ficha-sitio'
```
- Los 5 módulos que prueban los `*.spec.ts` todavía no existen. No hay otros errores de compilación de las
  pruebas. `app.spec.ts` se ajustó para comprobar solo que la app se crea con un `<router-outlet>`.

**Revisión del orquestador:** sin `skip`, `only` ni `xfail`; ninguna prueba llama a internet; la URL de la base de
pruebas llega por el entorno o por `backend/.env`, y si falta la prueba falla con un mensaje claro.

**Cobertura:** las 20 CA tienen prueba. Además hay pruebas de `GET /api/filtros` y de RF-012 (POST, PUT, PATCH y
DELETE → 405). Sin prueba automática, como dice el plan: CE-001, CE-004, CE-005, teclado (RF-011) y la espera de
300 ms del campo de búsqueda.

**Supuestos del `probador` que el `implementador` debe respetar** (no fijados en la spec, fijados por las pruebas):
nombres de tablas del modelo de datos; `crear_motor`, `crear_esquema` y `obtener_sesion` en `app/db.py`; mensajes
de `ErrorCarga` y de 422 que incluyen el nombre del campo; textos /cargando/i, /no se pudo|error/i y /reintentar/i;
enlace `a[href="/sitios"]` para volver; dos `<select>` con `value` = clave.

## Decisiones del grupo durante la spec
| # | Decisión | Razón |
|---|---|---|
| D-1 | Los precios de la Tatacoa y de San Agustín, publicados en 2024, se mantienen con `fecha_referencia_precio` 2026-11-24 y la nota «(dato de 2024)» en el concepto (2026-11-24). | El grupo lo eligió. La constitución pide la fecha en que se consultó, y el curador los consultó ese día; la nota avisa al turista que la tarifa publicada es de 2024. |
| D-2 | El catálogo queda con 10 sitios y 4 de las 7 categorías. | Cumple la spec (10 a 15). No se hallaron coordenadas verificables para sitios de aventura, cultura y gastronomía. |

## Hallazgos de los revisores
| # | Revisor | Hallazgo | Decisión |
|---|---|---|---|
| — | — | Pendiente (Fase 5). | — |
