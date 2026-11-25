---
description: "Tareas de la spec 001-catalogo-sitios"
---

# Tareas: Catálogo de sitios turísticos del Huila

**Entrada**: documentos de diseño en `specs/001-catalogo-sitios/` ([plan.md](plan.md), [spec.md](spec.md),
[research.md](research.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml),
[quickstart.md](quickstart.md)).

**Pruebas**: obligatorias (constitución, principio III, y TDD del principio IV). Todas las pruebas se escriben en
la fase Red y se suben en su propio commit **antes** de cualquier código.

**Organización**: por fase de trabajo (Preparación → Datos → Red → Green → Verificación → Cierre), porque la
constitución exige que el commit de pruebas preceda al del código. Dentro de Red y Green cada tarea lleva la
historia que sirve:

| Etiqueta | Historia | Prioridad |
|---|---|---|
| US1 | Ver la lista de sitios | P1 |
| US2 | Ver la ficha de un sitio | P1 |
| US3 | Filtrar y buscar sitios | P2 |
| US4 | Catálogo inicial con datos verificables | P1 |

**Formato**: `- [ ] Tnnn [P?] [US?] (Responsable) descripción con ruta`. `[P]` = se puede hacer en paralelo
(archivos distintos, sin dependencias pendientes). Una tarea solo se marca `[X]` con evidencia: prueba en verde
o commit.

---

## Fase 1: Preparación (orquestador, con permiso del grupo en cada comando)

**Propósito**: dejar el esqueleto y las herramientas para que los subagentes trabajen dentro de sus límites
(research D2, D3, D12, D13).

- [X] T001 (Orquestador) Crear `backend/requirements.txt` con las dependencias de research D13 y `backend/pytest.ini` con `pythonpath = .` y `testpaths = tests` (research D3)
- [X] T002 (Orquestador) Crear `backend/.env.example` con `DATABASE_URL`, `DATABASE_URL_PRUEBAS` y `ORIGENES_PERMITIDOS` sin valores reales
- [X] T003 (Orquestador) Ejecutar `uv venv` y `uv pip install -r requirements.txt` en `backend/` (crea `backend/.venv`, ignorado por git)
- [X] T004 (Orquestador) Crear el proyecto Angular 21 en `frontend/` con `ng new` (standalone, rutas, CSS, sin SSR, sin git propio) y ejecutar `npm install`; confirmar que existe `frontend/package-lock.json`
- [X] T005 (Orquestador) Crear `frontend/proxy.conf.json` (`/api` → `http://localhost:8000`) y enlazarlo en `frontend/angular.json` para `ng serve` (research D12)
- [X] T006 (Orquestador) Agregar el servicio `postgres:16` y la variable `DATABASE_URL_PRUEBAS` al job `backend` de `.github/workflows/ci.yml` (research D1)
- [X] T007 [P] (Orquestador) Copiar la tabla de comandos oficiales del plan a la sección Stack de `AGENTS.md`
- [X] T008 [P] (Orquestador) Actualizar `.claude/skills/datos-turisticos/SKILL.md` al formato de `data-model.md` (sin `aproximado`, municipio por clave, `valor_cop` desconocido = `null`) y los textos de vacío de `.claude/rules/frontend-angular.md` a los de la spec
- [X] T009 (Grupo) Crear en PostgreSQL local las bases `turismo` y `turismo_pruebas` y llenar `backend/.env` (ningún agente lo lee)
- [X] T010 (Orquestador) Comprobar que `cd backend && uv run pytest -q` y `cd frontend && npx ng test --watch=false` arrancan (sin pruebas propias aún) y hacer commit `chore:` con rutas explícitas

**Punto de control**: entorno listo; el CI encuentra `requirements.txt` y `package-lock.json`.

---

## Fase 2: Datos (curador-datos; en paralelo con la Fase 3)

**Propósito**: catálogo inicial real (US4, research D14). Formato en `data-model.md`, sección «Formato de los archivos de datos».

- [X] T011 [P] [US4] (curador-datos) Armar `backend/datos/municipios.json` con los 37 municipios del Huila (`data-model.md` `municipio.clave`, `municipio.nombre`) y su fuente
- [X] T012 [P] [US4] (curador-datos) Armar `backend/datos/sitios.json` con 10 a 15 sitios reales, incluido el Desierto de la Tatacoa, cumpliendo `data-model.md` `sitio.*`, `precio.*` y `fuente.url`; datos desconocidos en `null`, textos propios
- [X] T013 [US4] (Orquestador) Revisar que cada ficha tenga fuente y hacer commit `feat:` de los datos con rutas explícitas

---

## Fase 3: Red (probador)

**Propósito**: una prueba por criterio según la tabla *Criterio → prueba* del plan. Cada prueba debe **fallar
por falta de código** (`ModuleNotFoundError`, 404 de ruta inexistente, componente inexistente), no por errores
de sintaxis o de configuración.

### Backend
- [X] T014 (probador) Escribir `backend/tests/conftest.py`: base de pruebas desde `DATABASE_URL_PRUEBAS`, esquema limpio por sesión, `TestClient` y fixture con sitios semilla propios (no los de `backend/datos/`)
- [X] T015 [P] [US2] (probador) Escribir `backend/tests/test_texto.py`: `test_ca12_normalizar` y `test_ca20_slug` (CA-12, CA-20)
- [X] T016 [P] [US4] (probador) Escribir `backend/tests/test_carga.py`: CA-17, CA-18 y CA-19, incluidos los bordes inclusivos, el todo o nada y los límites de longitud de `nombre` (120) y `concepto` (80)
- [X] T017 [P] [US4] (probador) Escribir `backend/tests/test_datos.py`: CA-16 sobre los archivos reales de `backend/datos/`
- [X] T018 [P] [US1] (probador) Escribir en `backend/tests/test_sitios.py` las pruebas de lista: CA-1, CA-3, CA-4 y CA-5
- [X] T019 [US2] (probador) Agregar a `backend/tests/test_sitios.py` las pruebas de ficha: CA-6, CA-8, CA-9 y CA-20
- [X] T020 [US3] (probador) Agregar a `backend/tests/test_sitios.py` las pruebas de filtros: CA-10 a CA-13 y CA-15, además de `GET /api/filtros`

### Frontend
- [X] T021 [P] [US1] (probador) Escribir `frontend/src/app/utils/precio.spec.ts`: CA-2, CA-3 y CA-4 (12 meses, «Desde», «Gratis (hay otras tarifas)»)
- [X] T022 [P] [US2] (probador) Escribir `frontend/src/app/utils/mapa.spec.ts`: CA-7
- [X] T023 [P] [US3] (probador) Escribir `frontend/src/app/services/sitios.service.spec.ts`: CA-10 y CA-13 con `HttpTestingController`
- [X] T024 [P] [US1] (probador) Escribir `frontend/src/app/pages/lista-sitios/lista-sitios.spec.ts`: CA-1, CA-5 y CA-14
- [X] T025 [P] [US2] (probador) Escribir `frontend/src/app/pages/ficha-sitio/ficha-sitio.spec.ts`: CA-6, CA-7, CA-8, CA-9 y CA-20

### Evidencia Red
- [X] T026 (Orquestador) Crear `specs/001-catalogo-sitios/revision.md` desde `docs/plantillas/revision.md`, ejecutar ambas suites, comprobar que fallan por el motivo esperado, anotar la salida en `revision.md` y hacer commit `test:` solo con las pruebas

**Punto de control**: las 20 CA tienen prueba y todas están en rojo por la razón correcta.

---

## Fase 4: Green (implementador)

**Propósito**: código mínimo para poner las pruebas en verde. Base común primero; después cada historia.
Si la verificación falla, máximo 2 vueltas y luego se consulta al grupo.

### Base común del backend (bloquea US1 a US4)
- [X] T027 (implementador) Crear `backend/db/001_esquema.sql` con las 4 tablas y sus `CHECK`, `UNIQUE` y FK (`data-model.md` `municipio.*`, `sitio.*`, `precio.*`, `fuente.*`)
- [X] T028 (implementador) Crear `backend/app/config.py` (pydantic-settings) y `backend/app/db.py` (motor, sesión, `crear_esquema()`)
- [X] T029 [P] (implementador) Crear `backend/app/texto.py` con `normalizar()` y `slug()` (research D5 y D6; `data-model.md` `sitio.slug`, `sitio.nombre_normalizado`)
- [X] T030 [P] (implementador) Crear `backend/app/catalogos.py` con las 7 categorías clave → etiqueta (`data-model.md`, sección «Categorías»; `sitio.categoria`)
- [X] T031 (implementador) Crear `backend/app/modelos.py` (tablas SQLAlchemy) y `backend/app/esquemas.py` (Pydantic: `Opcion`, `SitioResumen`, `SitioDetalle`, `Error`, según `contracts/openapi.yaml`)
- [X] T032 (implementador) Crear `backend/app/main.py` con la app, CORS desde `ORIGENES_PERMITIDOS` y manejadores de 404 y 422 con `{"detalle": …}` en español (research D11)

### US4: Carga validada del catálogo
- [X] T033 [US4] (implementador) Agregar `FichaSitio` a `backend/app/esquemas.py` y crear `backend/app/carga.py` con `cargar_catalogo()`, `ErrorCarga` y `__main__`, aplicando las reglas de rechazo de `data-model.md` (`sitio.nombre`, `sitio.latitud`, `sitio.longitud`, `sitio.descripcion`, `sitio.fecha_referencia_precio`, `precio.valor_cop`, `precio.concepto`, `fuente.url`; research D9 y D10). Pasan CA-16 a CA-19

### US1: Lista de sitios
- [X] T034 [US1] (implementador) Crear `backend/app/repositorio.py` (lista ordenada por `sitio.nombre_normalizado` y precio de referencia = menor `precio.valor_cop`) y `GET /api/sitios` en `backend/app/rutas/sitios.py`. Pasan CA-1, CA-3, CA-4 y CA-5 del backend
- [X] T035 [P] [US1] (implementador) Crear `frontend/src/app/models/sitio.ts` según `contracts/openapi.yaml` y `frontend/src/app/utils/precio.ts` (research D8). Pasan CA-2, CA-3 y CA-4 del frontend
- [X] T036 [US1] (implementador) Crear `frontend/src/app/services/sitios.service.ts` y `frontend/src/app/pages/lista-sitios/` (signals, OnPush, estados de carga, vacío y error con reintentar; móvil primero), con la ruta `sitios` en `frontend/src/app/app.routes.ts`. Pasan CA-1 y CA-5 del frontend

### US2: Ficha del sitio
- [X] T037 [US2] (implementador) Agregar `GET /api/sitios/{slug}` a `backend/app/rutas/sitios.py` (404 si `sitio.slug` no existe o es inválido). Pasan CA-6, CA-8, CA-9 y CA-20 del backend
- [X] T038 [P] [US2] (implementador) Crear `frontend/src/app/utils/mapa.ts` (research D12). Pasa CA-7
- [X] T039 [US2] (implementador) Crear `frontend/src/app/pages/ficha-sitio/` con la ruta `sitios/:slug` (`loadComponent`): «No disponible», «Sitio no encontrado» con enlace a la lista, fuentes como enlaces y «Ver en mapa» con `target="_blank"` y `rel="noopener noreferrer"`. Pasan CA-6 a CA-9 y CA-20 del frontend

### US3: Filtros y búsqueda
- [X] T040 [US3] (implementador) Agregar a `backend/app/repositorio.py` y `backend/app/rutas/sitios.py` los filtros `municipio`, `categoria` y `q` (`LIKE` escapado sobre `sitio.nombre_normalizado`; 422 en español; `q` ≤ 100) y `GET /api/filtros`. Pasan CA-10 a CA-13 y CA-15
- [X] T041 [US3] (implementador) Agregar a `sitios.service.ts` y `lista-sitios/` los selectores de municipio y categoría, la búsqueda con espera de 300 ms, los filtros en los parámetros de la URL, el mensaje sin resultados y «Limpiar filtros». Pasan CA-10, CA-13 y CA-14 del frontend

### Evidencia Green
- [X] T042 (implementador) Refactor sin cambiar comportamiento, con `uv run ruff check` y `npm run build` limpios
- [X] T043 (Orquestador) Ejecutar ambas suites en verde, anotar la salida en `revision.md` y hacer commit `feat:` del código con rutas explícitas

---

## Fase 5: Verificación

- [ ] T044 (Orquestador y grupo) Cargar el catálogo real con `uv run python -m app.carga` y recorrer `quickstart.md`: escenarios 1 a 9, 360 px, teclado, contraste AA y tiempos (CE-001, CE-004, CE-005, RF-011)
  - **Pendiente:** el grupo decidió pasar al Cierre sin la prueba manual (2026-11-24); queda anotada en el PR.
- [X] T045 [P] (revisor-pull-request) Revisar la rama contra la spec, la constitución y la evidencia
- [X] T046 [P] (revisor-seguridad) Revisar los endpoints, las consultas SQL, CORS, `.env.example` y la validación de entrada
- [X] T047 (Orquestador) Anotar cada hallazgo en `specs/001-catalogo-sitios/revision.md` como aceptado (con commit) o descartado (con razón); los aceptados se corrigen con `probador` o `implementador` según corresponda

---

## Fase 6: Cierre

- [X] T048 (Orquestador) Crear `specs/001-catalogo-sitios/skills.md` desde `docs/plantillas/skills.md`
- [X] T049 (Orquestador) Marcar `[X]` en este archivo solo las tareas con evidencia
- [X] T050 (registrador-prompts) Actualizar `docs/prompts/` con la sesión de la spec 001 (y corregir el commit citado en el prompt 7 de la sesión 001)
- [ ] T051 (Orquestador) Mostrar `git status --short -uall`, proponer los `git add` por ruta, los commits y el push, y abrir el PR hacia `recuperacion/olaya` con `.github/pull_request_template.md`. **No fusionar.**

---

## Dependencias y orden

```text
Fase 1 Preparación ──► Fase 2 Datos ─────────────┐
                  └──► Fase 3 Red (T014 primero) ─┴─► T026 commit test: ──► Fase 4 Green
Fase 4: base T027–T032 ──► US4 (T033) ──► US1 (T034–T036) ──► US2 (T037–T039) ──► US3 (T040–T041) ──► T042–T043
──► Fase 5 Verificación ──► Fase 6 Cierre
```
- CA-16 (`test_datos.py`) solo pasa a verde cuando la Fase 2 está completa.
- US2 y US3 usan el repositorio y la ruta que crea US1 (T034); US3 modifica la pantalla de US1 (T036).
- En el frontend, T035 y T038 son funciones puras independientes y pueden hacerse en cualquier orden.

## Paralelo
- **Fase 2 y Fase 3** al mismo tiempo: el `curador-datos` y el `probador` escriben en carpetas distintas.
- **Red:** después de T014, las tareas T015–T018 y T021–T025 son archivos distintos y se pueden hacer en paralelo.
- **Verificación:** los dos revisores (T045 y T046) en paralelo.

## Estrategia
- **MVP:** base común + US4 + US1 + US2, es decir, catálogo real, lista y ficha (todas P1). US3 (filtros) completa la spec.
- Un solo PR para toda la spec 001, como pide el flujo del proyecto; los commits siguen el orden test → feat.
