# Turismo Huila — Proyecto de recuperación, Grupo 10

Plataforma web de **sitios turísticos del Huila (Colombia)**: catálogo con precios aproximados en COP,
ubicación en mapa, horarios y cómo llegar, más un asistente con IA que arma itinerarios solo con los datos
del catálogo.

**Stack:** Angular · FastAPI (Python) · PostgreSQL · API de Claude.

Construido con un flujo de ingeniería asistida por IA: **Claude Code** dentro de VS Code,
**Spec-Driven Development con GitHub Spec Kit**, subagentes con permisos limitados por hooks, skills propias y
registro de cada prompt.

## El arnés de IA

| Pieza | Qué es | Dónde está |
|---|---|---|
| Constitución | Principios no negociables del proyecto | `.specify/memory/constitution.md` |
| Memoria | Lo que Claude lee al empezar | `AGENTS.md` y `CLAUDE.md` |
| Reglas | Normas que se cargan al tocar ciertos archivos | `.claude/rules/` |
| Skills | Procedimientos: Spec Kit (9) y del grupo (4) | `.claude/skills/` |
| Agentes | Orquestador + 7 subagentes con rol y permisos propios | `.claude/agents/` |
| Hooks y permisos | Controles que bloquean lo prohibido | `.claude/hooks/` y `.claude/settings.json` |
| Comando | `/nueva-spec NNN-nombre`: el flujo completo de una spec | `.claude/commands/` |
| Specs | Spec, plan, tareas y evidencia por funcionalidad | `specs/NNN-nombre/` |
| Prompts | Registro textual de cada sesión con Claude Code | `docs/prompts/` |
| Calidad | CI y plantilla de Pull Request | `.github/` |

El mapa detallado está en [`docs/ARNES.md`](docs/ARNES.md).

## Cómo se trabaja una funcionalidad
1. Abrir Claude Code en la carpeta del proyecto y escribir `/nueva-spec 001-catalogo-sitios`.
2. Prompt con la fórmula *qué quiero, para quién, contexto, formato y restricciones*.
3. `/speckit-specify` → `/speckit-clarify` → el grupo aprueba la spec.
4. El `explorador` busca lo reutilizable → `/speckit-plan` → el grupo aprueba el plan.
5. `/speckit-tasks` → `/speckit-analyze`.
6. El `probador` escribe las pruebas (Red, commit propio) → el `implementador` el código (Green).
7. `revisor-pull-request` y `revisor-seguridad` → decisiones en `revision.md`.
8. Pull Request hacia `recuperacion/olaya` con la plantilla y el CI en verde.

## Specs

| # | Spec | Estado | PR |
|---|---|---|---|
| 001 | Catálogo de sitios turísticos | En curso | — |
| 002 | Asistente de itinerarios con IA | Pendiente | — |
| 003 | Administración de sitios (opcional) | Pendiente | — |

## Comandos
```bash
node --test .claude/hooks/hooks.test.mjs   # pruebas de los hooks del arnés
```
Los comandos del backend y del frontend se agregan cuando el plan de la spec 001 los fije.
