# CLAUDE.md — Proyecto de recuperación, Grupo 10

## Qué es el proyecto
Plataforma web de **sitios turísticos del Huila (Colombia)**: ficha de cada sitio con
ubicación, precio aproximado (COP), categoría, municipio, horarios y cómo llegar.
Proyecto académico del curso de Ingeniería de IA y sistemas agénticos.

## Flujo de trabajo obligatorio (Spec-Driven Development con Spec Kit)
Toda funcionalidad nueva sigue este orden; no se escribe código sin spec, plan y tareas:
1. `/speckit-constitution` — principios (solo se ajusta si cambian las reglas del proyecto).
2. `/speckit-specify` — el QUÉ y el PARA QUIÉN, sin tecnología.
3. `/speckit-clarify` — resolver ambigüedades antes de planear.
4. `/speckit-plan` — el CÓMO: arquitectura, modelo de datos, librerías.
5. `/speckit-tasks` — tareas numeradas y verificables.
6. `/speckit-analyze` — coherencia spec ↔ plan ↔ tareas.
7. `/speckit-implement` — implementación tarea por tarea.

Las specs viven en `specs/NNN-nombre/` (spec.md, plan.md, tasks.md). La constitución en
`.specify/memory/constitution.md` manda sobre cualquier otra regla.

## Registro de prompts (evidencia del curso)
- Cada sesión de trabajo se registra en `docs/prompts/` (ver `docs/prompts/README.md`).
- Registrar el prompt del usuario **textual**, qué hizo Claude y el commit resultante.

## Git y GitHub
- Rama de trabajo: `recuperacion/olaya`. `main` solo recibe cambios por Pull Request.
- Commits pequeños, en español, con prefijo convencional: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- Nunca subir secretos (`.env`, tokens, llaves de API).
- No copiar código ni contenido de otros repositorios: todo se construye desde cero en este repo.

## Convenciones
- Idioma de la interfaz, documentación y commits: **español**.
- Precios siempre en pesos colombianos (COP) y marcados como *aproximados*, con fecha de referencia.
- Datos de sitios: solo información verificable; si un dato no se conoce, se deja vacío, no se inventa.
- Stack técnico: se decide en `/speckit-plan` y se documenta aquí cuando esté aprobado.
