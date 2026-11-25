# Arnés del agente en Turismo Huila

El **arnés** es todo lo que rodea a Claude Code en este repositorio para que trabaje bien: qué le dice qué
hacer, qué le impide hacer, cómo se comprueba su trabajo y dónde queda la evidencia.

## Las cuatro capas

| Capa | Para qué sirve | Dónde está |
|---|---|---|
| **Guía** | Que el agente conozca el proyecto y sus reglas | Constitución, `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.claude/commands/` |
| **Control** | Que no pueda hacer lo que nunca debe hacerse | `.claude/settings.json` (permisos) y `.claude/hooks/` |
| **Verificación** | Que el trabajo se compruebe solo | pytest, vitest, pruebas de los hooks y `.github/workflows/ci.yml` |
| **Proceso** | Que cada cambio sea trazable y revisable | Spec Kit en `specs/NNN-nombre/`, `docs/prompts/`, ramas `feat/NNN-*` y Pull Requests |

## 1. Guía

### Memoria
- `.specify/memory/constitution.md`: 5 principios no negociables (SDD, datos verificables, pruebas y contratos, trazabilidad agéntica, seguridad y simplicidad).
- `AGENTS.md`: stack, ramas, agentes, evidencia y lo que el agente NO debe hacer.
- `CLAUDE.md`: importa `AGENTS.md` con `@AGENTS.md` y agrega reglas propias de Claude Code.

### Reglas (`.claude/rules/`)
| Regla | Se carga al tocar |
|---|---|
| `flujo-y-git.md` | Siempre |
| `pruebas.md` | `backend/tests/**`, `frontend/src/**/*.spec.ts` |
| `backend-api.md` | `backend/app/**` |
| `frontend-angular.md` | `frontend/src/**` |

### Skills (`.claude/skills/`)
| Skill | Origen | Para qué |
|---|---|---|
| `speckit-*` (9) | GitHub Spec Kit | Flujo de Spec-Driven Development |
| `datos-turisticos` | Del grupo | Formato y validación de la ficha de un sitio |
| `escribir-pruebas` | Del grupo | Pruebas desde los criterios de aceptación |
| `crear-endpoint-fastapi` | Del grupo | Endpoints del backend |
| `crear-pantalla-angular` | Del grupo | Pantallas del frontend |

### Subagentes (`.claude/agents/`)
| Agente | Modelo | Rol | Límite |
|---|---|---|---|
| `explorador` | haiku | Encuentra lo reutilizable antes de planear | Solo lectura (sin Edit/Write/Bash) |
| `curador-datos` | sonnet | Fichas de sitios con fuentes | Hook: solo `backend/datos/**` |
| `probador` | sonnet | Pruebas primero (Red) | Hook: solo archivos de prueba y comandos de prueba |
| `implementador` | sonnet | Código mínimo (Green) y refactor | Hook: `backend/**` y `frontend/**` sin pruebas; solo pruebas, lint y build |
| `revisor-pull-request` | haiku | Revisión antes del PR | Solo lectura |
| `revisor-seguridad` | opus | API, base de datos, secretos e IA | Solo lectura |
| `registrador-prompts` | haiku | Evidencia en `docs/prompts/` | — |

El **orquestador** es la sesión principal de Claude Code: coordina y no programa. Se controla con el modo
plan (no edita hasta que el grupo aprueba), con las reglas y con los permisos de `settings.json`.

### Comandos (`.claude/commands/`)
- `/nueva-spec NNN-nombre`: encadena prompt → `/speckit-specify` → `/speckit-clarify` → explorador →
  `/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → probador (Red) → implementador (Green) →
  revisores → evidencia → Pull Request, pidiendo aprobación en cada paso.

## 2. Control
- `.claude/settings.json`: permite sin preguntar solo la lectura de git y las pruebas de los hooks; niega leer o
  editar `.env`, `git push --force` y `git reset --hard`.
- `.claude/hooks/proteger-secretos.mjs` (toda la sesión): bloquea leer/editar/mostrar `.env` (salvo `.env.example`),
  `git push --force`, `git reset --hard` y `git add .` / `git add -A`.
- `.claude/hooks/limitar-agente.mjs` (por subagente): hace cumplir en qué carpetas escribe y qué comandos ejecuta
  cada agente. El campo `tools` de un agente solo dice *qué herramientas* tiene, no *sobre qué archivos*: por eso
  hace falta el hook.

## 3. Verificación
- `node --test .claude/hooks/hooks.test.mjs`: pruebas de los hooks (también corren en el CI).
- Backend: pytest. Frontend: vitest y build de Angular. Los comandos exactos se fijan en el plan de la spec 001.
- `.github/workflows/ci.yml`: repite todo en cada Pull Request.

## 4. Proceso y evidencia
Cada spec en `specs/NNN-nombre/`:

| Archivo | Lo produce | Contenido |
|---|---|---|
| `prompt.md` | Orquestador + grupo | Pedido con la fórmula del curso |
| `spec.md` | `/speckit-specify` + `/speckit-clarify` | Qué y para quién, criterios de aceptación |
| `plan.md` | `/speckit-plan` | Arquitectura, contrato de API, modelo de datos, criterio → prueba |
| `tasks.md` | `/speckit-tasks` | Tareas Red, Green, Verificación y Cierre |
| `skills.md` | Orquestador | Skills, reglas y agentes usados |
| `revision.md` | Orquestador | Commits Red/Green y decisiones sobre cada hallazgo |

Plantillas de `prompt.md`, `skills.md` y `revision.md` en `docs/plantillas/`. El registro textual de cada
sesión de trabajo con Claude Code está en `docs/prompts/`.
