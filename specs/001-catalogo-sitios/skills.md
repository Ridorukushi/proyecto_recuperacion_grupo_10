# 001-catalogo-sitios: skills, reglas y agentes usados

| Pieza | Para qué se usó en esta spec |
|---|---|
| Comando `/nueva-spec` | Encadenó los 10 pasos (prompt → spec → explorar → plan → tareas → Red → Green → revisión → cierre), con confirmación del grupo en cada uno. |
| Skill `speckit-specify` | Generó `spec.md` desde `prompt.md`: 4 historias, CA-1 a CA-20 y checklist de calidad. |
| Skill `speckit-clarify` | 3 aclaraciones: 7 categorías, dirección legible `/sitios/<slug>` y precio de referencia «Desde». |
| Skill `speckit-plan` | `plan.md`, `research.md` (14 decisiones), `data-model.md`, `contracts/openapi.yaml`, `quickstart.md` y la tabla criterio → prueba. |
| Skill `speckit-tasks` | `tasks.md`: 51 tareas en 6 fases (Preparación, Datos, Red, Green, Verificación, Cierre). |
| Skill `speckit-analyze` | 9 hallazgos de consistencia; se corrigieron 7 antes del Red (commit `7ae0973`). |
| Skill `datos-turisticos` | Formato y reglas de la ficha, usado por el `curador-datos` y el `probador`; se actualizó al modelo de datos aprobado (`4527c45`). |
| Skill `escribir-pruebas` y regla `.claude/rules/pruebas.md` | Nombres `test_ca<n>_…`, aserciones de contenido, sin `skip`/`only`, sin internet. |
| Skill `crear-endpoint-fastapi` y regla `.claude/rules/backend-api.md` | `/api/sitios`, `/api/sitios/{slug}`, `/api/filtros`, Pydantic, consultas parametrizadas y errores en español. |
| Skill `crear-pantalla-angular` y regla `.claude/rules/frontend-angular.md` | Lista y ficha standalone con signals, servicio HTTP, estados de carga/vacío/error y accesibilidad; la regla se ajustó a los textos de la spec. |
| Regla `.claude/rules/flujo-y-git.md` | Rama `feat/001-catalogo-sitios`, `git add` por ruta, commit de pruebas antes del código. |
| Hook `limitar-agente.mjs` | Limitó qué escribe y ejecuta cada subagente (por eso la Preparación la hizo el orquestador, decisión D2 de `research.md`). |
| Hook `proteger-secretos.mjs` | Bloqueó un comando del orquestador que mencionaba `.env`; `backend/.env` lo creó el grupo. |
| Agente `explorador` | Informe de lo reutilizable (skills, reglas, CI y hook) y 22 huecos que el plan resolvió. |
| Agente `curador-datos` | 37 municipios y 10 sitios reales con fuentes (`a35851d`); decisiones D-1 y D-2 en `revision.md`. |
| Agente `probador` | Pruebas antes del código: Red `1776bc4` (126 pruebas) y Red de la revisión `2e7ec1e`; orden de imports `263ec20`. |
| Agente `implementador` | Código: Green `edac5e3` y correcciones de la revisión `558308b`, ambos en verde a la primera vuelta. |
| Agente `revisor-pull-request` | 14 hallazgos (1 alto); ver `revision.md`. |
| Agente `revisor-seguridad` | Se usó porque la spec agrega endpoints, base de datos y variables de entorno: 7 hallazgos (3 medios); ver `revision.md`. No hay IA en esta spec. |
| Agente `registrador-prompts` | Registro de la sesión en `docs/prompts/002-2026-11-24-spec-001-catalogo-sitios.md`. |
