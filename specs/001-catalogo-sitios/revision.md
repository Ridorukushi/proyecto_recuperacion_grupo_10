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
| `edac5e3` | **Green:** implementación (`implementador`, sin vueltas de corrección). |
| `2e7ec1e` · `558308b` | Arreglos tras la revisión: Red (`test:`) y Green (`fix:`), en verde a la primera vuelta. |

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

## Evidencia del Green
Ejecutado por el orquestador el 2026-11-24, después del informe del `implementador`.

| Comando | Resultado |
|---|---|
| `cd backend && uv run pytest -q` | **91 passed**, 1 warning (aviso de FastAPI sobre `httpx` en `TestClient`; no es nuestro) |
| `cd frontend && npx ng test --watch=false` | **37 passed** (6 archivos) |
| `cd frontend && npm run build` | Compila sin errores |
| `cd backend && uv run ruff check` | 1 aviso I001 en `backend/tests/conftest.py` (imports sin ordenar, archivo de prueba) |

**Bloqueo de entorno (no de código):** en el primer intento, 76 pruebas del backend no corrieron porque faltaba
`backend/.env`, y después porque la clave de `postgres` guardada no coincidía. Se resolvió creando un usuario
`turismo`, dueño de las bases `turismo` y `turismo_pruebas`, con su clave escrita en `.env` desde la misma variable.
No cuenta como vuelta de corrección del `implementador`.

**Decisiones del `implementador`:**
- Los mensajes de `ErrorCarga` conservan el texto de Pydantic (en inglés). Solo los ve quien carga el catálogo,
  no el turista.
- Si un sitio no tiene precios conocidos, `fecha_referencia_precio` se guarda en `NULL`.
- El orden usa `COLLATE "C"` sobre `nombre_normalizado`.
- Los filtros se escriben en la URL con `replaceUrl`, así que el botón Atrás no los restaura (YAGNI).

## Decisiones del grupo durante la spec
| # | Decisión | Razón |
|---|---|---|
| D-1 | Los precios de la Tatacoa y de San Agustín, publicados en 2024, se mantienen con `fecha_referencia_precio` 2026-11-24 y la nota «(dato de 2024)» en el concepto (2026-11-24). | El grupo lo eligió. La constitución pide la fecha en que se consultó, y el curador los consultó ese día; la nota avisa al turista que la tarifa publicada es de 2024. |
| D-2 | El catálogo queda con 10 sitios y 4 de las 7 categorías. | Cumple la spec (10 a 15). No se hallaron coordenadas verificables para sitios de aventura, cultura y gastronomía. |

## Hallazgos de los revisores
Revisores ejecutados el 2026-11-24 sobre `263ec20`. Las decisiones las tomó el grupo a partir de la recomendación
del orquestador. Los aceptados se corrigen en otra vuelta Red → Green (commits `test:` y `fix:`).

| # | Revisor | Sev. | Hallazgo | Decisión |
|---|---|---|---|---|
| R1 | `revisor-pull-request` | Alta | `python -m app.carga` borra las tablas antes de validar; si una ficha falla, el catálogo anterior se pierde. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R2 | `revisor-pull-request` | Media | Mensajes de `ErrorCarga` en inglés (texto de Pydantic). | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R3 | `revisor-pull-request` | Media | Un nombre sin letras ni dígitos produce un slug vacío y un error de BD sin formato. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R4 | `revisor-pull-request` | Media | Con un filtro inválido en la URL, «Reintentar» repite el 422 y el turista queda atrapado. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R5a | `revisor-pull-request` | Media | La lista muestra el precio del museo como precio del Desierto de la Tatacoa. | **Descartado:** decisión del grupo D-1; la ficha muestra el concepto «Entrada Museo de Historia Natural». |
| R5b | `revisor-pull-request` | Media | Sin evidencia de la consulta de los precios de Termales de Rivera. | **Descartado:** el `curador-datos` los consultó el 2026-11-24 en el sitio oficial, que figura como fuente de la ficha. |
| R6 | `revisor-pull-request` | Media | Las pruebas borran tablas aunque `DATABASE_URL_PRUEBAS` apunte por error a otra base. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R7 | `revisor-pull-request` | Baja | Un precio sin fecha se mostraría sin «aprox.». | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R8 | `revisor-pull-request` | Baja | Si `/api/filtros` falla, no hay aviso. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R9 | `revisor-pull-request` | Baja | `track p.concepto` duplica claves si se repite un concepto. | **Aceptado** (`558308b`, sin prueba automática: cambio de marcado o documentación) |
| R10 | `revisor-pull-request` | Baja | Los enlaces a otra pestaña no avisan a los lectores de pantalla. | **Aceptado** (`558308b`, sin prueba automática: cambio de marcado o documentación) |
| R11 | `revisor-pull-request` | Baja | La lista navega aunque los filtros no cambien. | **Descartado:** usa `replaceUrl`, no deja rastro en el historial ni tiene efecto visible (YAGNI). |
| R12 | `revisor-pull-request` | Baja | `match="nombre\|slug"` es poco estricto. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| R13 | `revisor-pull-request` | Sug. | Faltan pruebas de la recarga y del 422 en el frontend. | **Aceptado:** cubierto por las pruebas de R1 y R4. |
| R14 | `revisor-pull-request` | Sug. | `frontend/README.md` es el de `ng new`. | **Aceptado** (`558308b`, sin prueba automática: cambio de marcado o documentación) |
| S1 | `revisor-seguridad` | Media | `?q=%00` provoca un 500 en vez de un 422. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| S2 | `revisor-seguridad` | Media | `municipio` y `categoria` sin largo máximo; el 422 repite el valor completo. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| S3 | `revisor-seguridad` | Media | `001_esquema.sql` empieza con `DROP TABLE` y lo usa la carga. | **Aceptado** con R1 (`558308b`) |
| S4 | `revisor-seguridad` | Baja | `horario`, `como_llegar` y las URL de fuentes sin largo máximo. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
| S5 | `revisor-seguridad` | Baja | `*` en `ORIGENES_PERMITIDOS` abriría CORS. | **Aceptado:** aviso en `.env.example` (`558308b`) |
| S6 | `revisor-seguridad` | Baja | `/docs`, `/redoc` y `/openapi.json` públicos. | **Descartado:** API pública de solo lectura, sin secretos; el contrato ya es público en el repositorio y `/docs` sirve al curso. |
| S7 | `revisor-seguridad` | Baja | Los errores inesperados no siguen el formato `{"detalle": …}`. | **Aceptado** (`2e7ec1e` test, `558308b` fix) |
