# Turismo Huila — Proyecto de recuperación, Grupo 10

Plataforma web de **sitios turísticos del Huila (Colombia)**: catálogo con precio aproximado en COP,
ubicación en mapa, municipio, categoría, horario y cómo llegar, más un asistente con IA que arma
itinerarios solo con los datos del catálogo. Proyecto del curso de Ingeniería de IA y sistemas
agénticos.

> **Estado:** arnés y constitución listos. Spec en curso: `001-catalogo-sitios`.

## Reglas que mandan
1. `.specify/memory/constitution.md`: principios no negociables. Prevalece sobre este archivo.
2. `.claude/rules/`: normas por tipo de archivo. Se cargan solas al tocar esos archivos.
3. Este archivo: contexto del proyecto.

El mapa completo del arnés (memoria, reglas, skills, agentes, hooks y evidencia) está en
`docs/ARNES.md`.

## Stack
- **Frontend:** Angular (componentes standalone, signals, TypeScript estricto), en `frontend/`. Pruebas con vitest.
- **Backend:** Python 3.12 con FastAPI, en `backend/`. Pruebas con pytest.
- **Base de datos:** PostgreSQL. Esquema y migraciones versionados en `backend/`.
- **IA:** API de Claude, llamada solo desde el backend.

### Comandos oficiales (fijados en el plan de la spec 001)
| Para qué | Local (agentes y grupo) | CI |
|---|---|---|
| Pruebas backend | `cd backend && uv run pytest -q` | `python -m pytest -q` (con PostgreSQL 16 como servicio) |
| Lint backend | `cd backend && uv run ruff check` | — |
| Pruebas frontend | `cd frontend && npx ng test --watch=false` | igual |
| Compilar frontend | `cd frontend && npm run build` | igual |
| Pruebas de hooks | `node --test .claude/hooks/hooks.test.mjs` | igual |
| Cargar catálogo (solo grupo u orquestador) | `cd backend && uv run python -m app.carga` | — |
| Levantar la app | `cd backend && uv run uvicorn app.main:app --reload` y `cd frontend && npx ng serve` | — |

Las pruebas del backend necesitan PostgreSQL 16 local y `backend/.env` (copiado de `backend/.env.example`).

## Ramas y flujo
- `main`: versión entregable. Solo recibe Pull Requests desde `recuperacion/olaya`.
- `recuperacion/olaya`: rama de integración del grupo.
- Cada spec tiene su rama `feat/NNN-nombre`, que sale de `recuperacion/olaya` y vuelve a ella por Pull Request.
- Una spec nueva se arranca con `/nueva-spec NNN-nombre`, que encadena las skills `speckit-*` con los subagentes.

## Agentes
El orquestador es la sesión principal de Claude Code: coordina, no programa. Los subagentes de
`.claude/agents/` hacen el trabajo:

| Agente | Rol | Puede escribir |
|---|---|---|
| `explorador` | Busca lo que ya existe para reutilizarlo | Nada (solo lee) |
| `curador-datos` | Investiga y arma las fichas de sitios con fuentes | `backend/datos/` |
| `probador` | Escribe las pruebas antes del código (Red) | Solo archivos de prueba |
| `implementador` | Escribe el código mínimo que pasa las pruebas (Green) | `backend/` y `frontend/` sin pruebas |
| `revisor-pull-request` | Revisa la rama antes del PR | Nada (solo lee) |
| `revisor-seguridad` | Revisa API, base de datos, secretos y la llamada a la IA | Nada (solo lee) |
| `registrador-prompts` | Mantiene la evidencia de prompts | `docs/` |

Los límites de escritura y de comandos del `probador`, del `implementador` y del `curador-datos`
los hace cumplir el hook `.claude/hooks/limitar-agente.mjs`, no solo las instrucciones.

## Evidencia por spec
Cada spec vive en `specs/NNN-nombre/` con:
- `spec.md`, `plan.md` y `tasks.md`, generados por Spec Kit.
- `prompt.md`: el pedido con la fórmula *qué quiero, para quién, contexto, formato y restricciones*.
- `skills.md`: las skills, reglas y agentes usados y para qué.
- `revision.md`: el historial de commits Red/Green y cada hallazgo de los revisores con su decisión.

El registro textual de todas las sesiones está en `docs/prompts/`.

## Lo que el agente NO debe hacer
- Escribir código sin spec, plan aprobado y tareas.
- Inventar datos turísticos: precios, horarios o coordenadas desconocidos se dejan vacíos.
- Copiar código o textos de otros repositorios o sitios web.
- Leer, editar o mostrar archivos `.env` (solo `.env.example`).
- Usar `git add .`, `git push --force`, `git reset --hard` o fusionar a `main`.
- Llamar a la API de Claude desde el frontend.

## Convenciones
- Interfaz, documentación, specs y commits en **español**.
- Commits cortos con prefijo convencional: `feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`.
- Precio mostrado así: `$25.000 COP (aprox., consultado en nov. 2026)`. Sin precio: «Precio no disponible».
