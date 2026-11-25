# Plan de implementación: Catálogo de sitios turísticos del Huila

**Rama**: `feat/001-catalogo-sitios` | **Fecha**: 2026-11-24 | **Spec**: [spec.md](spec.md)

**Entrada**: spec aprobada en `specs/001-catalogo-sitios/spec.md` e informe del `explorador` (2026-11-24).

**Estado**: Aprobado por el grupo (2026-11-24), incluidas las 7 decisiones de research.md señaladas al grupo.

## Resumen

Catálogo de solo lectura de 10 a 15 sitios turísticos reales del Huila.
- **Backend:** FastAPI expone tres endpoints (`/api/sitios`, `/api/sitios/{slug}` y `/api/filtros`) sobre
  PostgreSQL. Una función de carga valida las fichas de `backend/datos/` (todo o nada) antes de guardarlas.
- **Frontend:** Angular tiene dos pantallas, lista con filtros y ficha.
- **Formato:** el precio se formatea en el frontend con una función pura. La búsqueda sin tildes y el slug
  salen de la misma normalización en el backend.

Detalle de cada decisión en [research.md](research.md); modelo en [data-model.md](data-model.md); contrato en
[contracts/openapi.yaml](contracts/openapi.yaml); validación de punta a punta en [quickstart.md](quickstart.md).

## Contexto técnico

**Lenguaje/versión**: Python 3.12 (backend); TypeScript estricto con Angular 21 (frontend).

**Dependencias principales**: FastAPI, Pydantic 2 + pydantic-settings, SQLAlchemy 2, psycopg 3, uvicorn;
Angular (lo que trae `ng new`). Sin librerías de mapas.

**Almacenamiento**: PostgreSQL 16. Esquema en `backend/db/001_esquema.sql`.

**Pruebas**:
- Backend: pytest con el `TestClient` de FastAPI, contra una base PostgreSQL real de pruebas
  (`DATABASE_URL_PRUEBAS`).
- Frontend: vitest mediante `ng test`.

**Plataforma**:
- Navegadores modernos, móvil primero.
- Desarrollo en Windows. El CI corre en Ubuntu con `postgres:16` como servicio.

**Tipo de proyecto**: aplicación web con `backend/` y `frontend/`.

**Objetivos de rendimiento**: lista y ficha completas en menos de 2 s con conexión móvil (CE-004).

**Restricciones**:
- Sin datos inventados.
- Errores en español con la forma `{"detalle": …}`.
- Los agentes solo ejecutan los comandos que permite `limitar-agente.mjs`.

**Escala**: 10 a 15 sitios, 37 municipios y 7 categorías. Sin paginación.

### Comandos oficiales (se copian a `AGENTS.md` en la fase Preparación)
| Para qué | Local (agentes y grupo) | CI |
|---|---|---|
| Pruebas backend | `cd backend && uv run pytest -q` | `python -m pytest -q` |
| Lint backend | `cd backend && uv run ruff check` | (no en esta spec) |
| Pruebas frontend | `cd frontend && npx ng test --watch=false` | igual |
| Compilar frontend | `cd frontend && npm run build` | igual |
| Pruebas de hooks | `node --test .claude/hooks/hooks.test.mjs` | igual |
| Cargar catálogo (solo grupo u orquestador) | `cd backend && uv run python -m app.carga` | — |

## Constitution Check

*Compuerta: se revisa antes de la Fase 0 y otra vez después del diseño.*

| Principio | Cómo lo cumple el plan | Estado |
|---|---|---|
| I. Desarrollo guiado por specs | Spec aprobada; este plan necesita aprobación; después vienen tasks y analyze. | ✅ |
| II. Datos verificables | COP aproximado con fecha (D8); coordenadas validadas en backend al cargar y con `CHECK` en la base (D9); fuente obligatoria; desconocido = `null`, nunca `0` (D8). | ✅ |
| III. Pruebas y contratos | OpenAPI en `contracts/` antes del código; pytest y vitest; tabla criterio → prueba abajo. | ✅ |
| IV. Trazabilidad agéntica | Red con `probador` en su propio commit, Green con `implementador`, curaduría con `curador-datos`; evidencia en `prompt.md`, `skills.md` y `revision.md`. | ✅ |
| V. Seguridad y simplicidad | `DATABASE_URL`, `DATABASE_URL_PRUEBAS` y `ORIGENES_PERMITIDOS` en `.env.example` sin valores reales; validación en el servidor; consultas parametrizadas y `LIKE` escapado; sin Alembic ni librerías de mapas (YAGNI); móvil primero y accesibilidad. | ✅ |

**Después del diseño:** sin violaciones de la constitución. Hay una excepción a `AGENTS.md`, justificada en
*Seguimiento de complejidad*.

## Estructura del proyecto

### Documentación (esta spec)
```text
specs/001-catalogo-sitios/
├── prompt.md · spec.md · plan.md · research.md · data-model.md · quickstart.md
├── contracts/openapi.yaml
├── checklists/requirements.md
├── tasks.md        # /speckit-tasks
├── skills.md       # Cierre
└── revision.md     # Revisores
```

### Código fuente
```text
backend/
├── requirements.txt · pytest.ini · .env.example
├── db/001_esquema.sql
├── datos/
│   ├── sitios.json            # curador-datos
│   └── municipios.json        # curador-datos
├── app/
│   ├── main.py                # FastAPI, CORS, manejadores de error, routers
│   ├── config.py              # pydantic-settings
│   ├── db.py                  # motor, sesión, crear_esquema()
│   ├── texto.py               # normalizar(), slug()
│   ├── catalogos.py           # 7 categorías (clave → etiqueta)
│   ├── esquemas.py            # Pydantic: FichaSitio (carga), SitioResumen, SitioDetalle, Opcion
│   ├── modelos.py             # tablas SQLAlchemy
│   ├── repositorio.py         # consultas
│   ├── carga.py               # cargar_catalogo(), ErrorCarga, __main__
│   └── rutas/sitios.py        # /api/sitios, /api/sitios/{slug}, /api/filtros
└── tests/
    ├── conftest.py            # base de pruebas, cliente, datos semilla
    ├── test_texto.py · test_carga.py · test_datos.py · test_sitios.py

frontend/                      # generado con ng new
├── proxy.conf.json
└── src/app/
    ├── app.routes.ts          # sitios, sitios/:slug (loadComponent)
    ├── models/sitio.ts
    ├── services/sitios.service.ts (+ .spec.ts)
    ├── utils/precio.ts (+ .spec.ts) · utils/mapa.ts (+ .spec.ts)
    └── pages/
        ├── lista-sitios/ (componente + .spec.ts)
        └── ficha-sitio/  (componente + .spec.ts)
```

**Decisión de estructura**: aplicación web con dos proyectos (`backend/` y `frontend/`). Las rutas
coinciden con lo que permite `limitar-agente.mjs`:
- `backend/tests/**` y `*.spec.ts` son del `probador`;
- el resto de `backend/` y `frontend/` es del `implementador`;
- `backend/datos/**` es del `curador-datos`.

## Fases y responsables

| Fase | Quién | Qué |
|---|---|---|
| **Preparación** | Orquestador, con permiso del grupo en cada comando | `uv venv`; `requirements.txt`, `pytest.ini`, `.env.example`; `uv pip install`; `ng new frontend`; `npm install`; `proxy.conf.json`; servicio PostgreSQL en `ci.yml`; comandos en `AGENTS.md`; ajustar la skill `datos-turisticos` y la regla `frontend-angular.md` al modelo nuevo. Commit `chore:`. |
| **Datos** | `curador-datos` | `municipios.json` (37) y `sitios.json` (10–15, con Tatacoa), con fuentes. Commit `feat:` de datos. Puede ir en paralelo con el Red. |
| **Red** | `probador` | Todas las pruebas de la tabla; deben fallar por falta de código (`ImportError`/404/componente inexistente), no por errores de sintaxis. Commit `test:` solo. |
| **Green** | `implementador` | Código mínimo hasta poner las pruebas en verde, más `ruff check` y `npm run build`. Máximo 2 vueltas si falla la verificación. Commit `feat:`. |
| **Verificación** | Orquestador y grupo | Suites completas, quickstart manual (360 px, teclado), `revisor-pull-request` y `revisor-seguridad`. |
| **Cierre** | Orquestador y `registrador-prompts` | `skills.md`, `revision.md`, tareas `[X]` con evidencia, `docs/prompts/` y PR hacia `recuperacion/olaya`. |

## Criterio → prueba

Backend: `backend/tests/`. Frontend: `frontend/src/app/`. Los nombres siguen `test_ca<n>_…` y los `it` del
frontend empiezan con `CA-n`.

| CA | Qué se verifica | Prueba(s) |
|---|---|---|
| CA-1 | Lista ordenada por nombre normalizado con nombre, municipio, categoría y precio de referencia | `test_sitios.py::test_ca1_lista_ordenada_con_campos`; `lista-sitios.spec.ts` «CA-1 muestra cada sitio con sus 4 datos» |
| CA-2 | `$25.000 COP (aprox., consultado en nov. 2026)` y «Desde» con varios precios | `precio.spec.ts` «CA-2 formatea precio conocido», «CA-2 antepone Desde», «CA-2 abrevia los 12 meses» |
| CA-3 | Desconocido: `null` en la API y «Precio no disponible», nunca «$0» | `test_sitios.py::test_ca3_precio_desconocido_es_null`; `precio.spec.ts` «CA-3 precio no disponible» |
| CA-4 | Gratis (0) distinto de desconocido | `test_sitios.py::test_ca4_precio_cero_no_es_null`; `precio.spec.ts` «CA-4 gratis», «CA-4 gratis con otras tarifas» |
| CA-5 | Catálogo vacío devuelve `[]`; estados de carga, vacío y error con reintentar | `test_sitios.py::test_ca5_catalogo_vacio`; `lista-sitios.spec.ts` «CA-5 carga», «CA-5 vacío», «CA-5 error y reintentar» |
| CA-6 | Ficha con todos los campos, precios con concepto y fuentes como enlaces | `test_sitios.py::test_ca6_ficha_completa`; `ficha-sitio.spec.ts` «CA-6 muestra la ficha completa» |
| CA-7 | URL de OpenStreetMap, `target=_blank` y `rel=noopener` | `mapa.spec.ts` «CA-7 arma la URL»; `ficha-sitio.spec.ts` «CA-7 enlace Ver en mapa» |
| CA-8 | Horario o cómo llegar `null` se muestra como «No disponible» | `test_sitios.py::test_ca8_campos_desconocidos_null`; `ficha-sitio.spec.ts` «CA-8 No disponible» |
| CA-9 | Slug inexistente o inválido: 404 «Sitio no encontrado.»; pantalla con enlace a la lista | `test_sitios.py::test_ca9_slug_inexistente_404`, `test_ca9_slug_invalido_404`; `ficha-sitio.spec.ts` «CA-9 no encontrado» |
| CA-10 | Filtro por municipio | `test_sitios.py::test_ca10_filtra_por_municipio`; `sitios.service.spec.ts` «CA-10 envía municipio» |
| CA-11 | Filtro por categoría | `test_sitios.py::test_ca11_filtra_por_categoria` |
| CA-12 | Búsqueda sin distinguir mayúsculas, minúsculas ni tildes; `%` y `_` literales; vacío = sin filtro | `test_texto.py::test_ca12_normalizar`; `test_sitios.py::test_ca12_busca_sin_tildes_ni_mayusculas`, `test_ca12_comodines_literales`, `test_ca12_busqueda_vacia` |
| CA-13 | Los tres filtros combinados | `test_sitios.py::test_ca13_filtros_combinados`; `sitios.service.spec.ts` «CA-13 envía los tres filtros» |
| CA-14 | Sin resultados: mensaje y «Limpiar filtros» | `lista-sitios.spec.ts` «CA-14 sin resultados y limpiar» |
| CA-15 | 422 en español si el municipio o la categoría no existen o si `q` pasa de 100 caracteres | `test_sitios.py::test_ca15_municipio_invalido_422`, `test_ca15_categoria_invalida_422`, `test_ca15_busqueda_larga_422` |
| CA-16 | `sitios.json` real: 10–15 fichas válidas con fuente, incluye Tatacoa; 37 municipios | `test_datos.py::test_ca16_catalogo_inicial_valido`, `test_ca16_municipios_del_huila` |
| CA-17 | Coordenadas fuera del Huila (y bordes inclusivos aceptados) | `test_carga.py::test_ca17_coordenadas_fuera_rechazadas` (parametrizada), `test_ca17_bordes_aceptados` |
| CA-18 | Sin fuente, sin nombre, municipio o categoría inválidos; ninguna ficha guardada | `test_carga.py::test_ca18_campos_invalidos_rechazados` (parametrizada), `test_ca18_todo_o_nada` |
| CA-19 | Precio sin fecha, precio negativo, nombre o slug repetido | `test_carga.py::test_ca19_precio_sin_fecha`, `test_ca19_precio_negativo`, `test_ca19_nombre_repetido` |
| CA-20 | `slug("Desierto de la Tatacoa")`, GET por slug y ruta `/sitios/:slug` del frontend | `test_texto.py::test_ca20_slug`; `test_sitios.py::test_ca20_ficha_por_slug`; `ficha-sitio.spec.ts` «CA-20 carga el sitio del parámetro slug» |

**Sin prueba automática (se verifica en Verificación con el quickstart):**
- CE-001 (encontrar un sitio en menos de 30 s);
- CE-004 (menos de 2 s);
- CE-005 (360 px sin desplazamiento horizontal);
- navegación con teclado (RF-011).

## Riesgos
- **Sin PostgreSQL local:** si un integrante no tiene PostgreSQL instalado, las pruebas del backend no corren en su
  computador. Mitigación: el quickstart y el CI.
- **Red sin datos:** `test_datos.py` falla en Red hasta que el `curador-datos` entregue los datos. Es el fallo
  esperado.
- **Fuentes poco confiables:** las fichas pueden quedar con campos `null` si no hay fuentes confiables; está
  permitido y preferible a inventar.

## Seguimiento de complejidad

| Excepción | Por qué se necesita | Alternativa más simple descartada porque |
|---|---|---|
| El orquestador escribe archivos (configuración, `ng new`, `ci.yml`, `AGENTS.md`), aunque `AGENTS.md` dice que «coordina, no programa». | Los hooks impiden a los subagentes instalar dependencias, crear el proyecto Angular y tocar `.github/`. | Ampliar los permisos de los agentes debilita el control que exige el principio IV (decisión del grupo, 2026-11-24). El orquestador no escribe lógica ni pruebas. |
