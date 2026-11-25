# Constitución — Turismo Huila (Proyecto de recuperación, Grupo 10)

Plataforma web de sitios turísticos del Huila (Colombia) con catálogo, precios aproximados,
ubicaciones y un asistente de itinerarios con IA.

## Core Principles

### I. Desarrollo guiado por especificaciones (NO NEGOCIABLE)

- Ninguna funcionalidad se implementa sin pasar por el flujo de Spec Kit:
  `specify → clarify → plan → tasks → analyze → implement`.
- Cada funcionalidad vive en `specs/NNN-nombre/` con `spec.md`, `plan.md` y `tasks.md`.
- La spec describe el QUÉ y el PARA QUIÉN sin tecnología; el plan describe el CÓMO.
- Si el código y la spec divergen, se corrige primero la spec y luego el código.

**Razón:** el curso evalúa el proceso de ingeniería con IA, no solo el resultado; las specs son
la fuente de verdad que guía a los agentes.

### II. Datos turísticos verificables

- Todo precio se expresa en pesos colombianos (COP), se rotula como *aproximado* y lleva la fecha
  de referencia en que se consultó.
- Las coordenadas MUST estar dentro del departamento del Huila
  (latitud 1.5 a 3.9, longitud −76.6 a −74.4) y se validan en backend.
- Cada sitio registra la fuente del dato. Un dato desconocido se deja vacío; nunca se inventa.
- El asistente con IA MUST responder solo con información del catálogo y decir explícitamente
  cuando no tiene un dato.

**Razón:** un turista toma decisiones de dinero y desplazamiento con esta información; un dato
inventado (incluida una alucinación del modelo) es un defecto grave.

### III. Pruebas y contratos de API

- Cada funcionalidad incluye pruebas automatizadas: backend con `pytest`, frontend con `vitest`.
- La API se diseña contract-first: el contrato OpenAPI se define en el plan antes de implementar
  y el frontend consume solo lo que el contrato expone.
- Ninguna tarea se marca como terminada si sus pruebas fallan o no existen.

**Razón:** las pruebas son la evidencia verificable de que lo que generan los agentes funciona.

### IV. Desarrollo agéntico trazable

- Los roles recurrentes se implementan como subagentes en `.claude/agents/` y el conocimiento
  reutilizable como skills en `.claude/skills/`.
- Cada sesión de trabajo con IA se registra en `docs/prompts/` con el prompt textual, lo que hizo
  el agente y el commit resultante.
- Commits pequeños, en español, con prefijo convencional (`feat:`, `fix:`, `docs:`, `chore:`,
  `test:`, `refactor:`).
- Ramas: cada spec se construye en `feat/NNN-nombre`, que sale de `recuperacion/olaya` y vuelve a ella
  por Pull Request. `recuperacion/olaya` llega a `main` por Pull Request. Ningún agente fusiona.
- Separación de roles (TDD): el subagente `probador` escribe las pruebas antes del código (Red) y se
  suben en su propio commit; el `implementador` escribe el código mínimo que las hace pasar (Green).
  Los límites de cada agente los hacen cumplir hooks, no solo instrucciones.
- Cada spec deja evidencia en su carpeta: `prompt.md`, `skills.md` y `revision.md`, además de
  `spec.md`, `plan.md` y `tasks.md`.
- Todo el código se escribe en este repositorio; no se copia código de otros repositorios.

**Razón:** la trazabilidad prompt → spec → commit es el entregable central del curso.

### V. Seguridad y simplicidad

- Los secretos (llave de la API de Claude, credenciales de base de datos) viven solo en variables
  de entorno; `.env` nunca se sube y existe un `.env.example` sin valores reales.
- Se valida toda entrada del usuario en backend; el frontend no es la única barrera.
- YAGNI: se construye solo lo que pide una spec aprobada. Sin abstracciones especulativas.
- Interfaz responsive (móvil primero) y accesibilidad básica: texto alternativo en imágenes,
  contraste suficiente y navegación con teclado.

**Razón:** el proyecto es público en GitHub y lo usarán turistas desde el celular.

## Stack y restricciones técnicas

- **Frontend:** Angular (componentes standalone, signals, TypeScript estricto), en `frontend/`.
- **Backend:** Python con FastAPI, en `backend/`.
- **Base de datos:** PostgreSQL, con esquema versionado en el repositorio.
- **IA en la aplicación:** API de Claude, invocada solo desde el backend (nunca desde el navegador).
- **Idioma:** interfaz, documentación, specs y commits en español.
- Cambiar una pieza del stack requiere enmendar esta constitución.

## Flujo de trabajo y calidad

1. Toda funcionalidad nueva abre su carpeta en `specs/` con `/speckit-specify`.
2. Antes de `/speckit-implement` se ejecuta `/speckit-analyze` y se resuelven sus hallazgos críticos.
3. Antes de abrir un Pull Request: pruebas en verde, revisión con el subagente revisor y prompt
   registrado en `docs/prompts/`.
4. Cada Pull Request enlaza la spec que implementa.

## Governance

- Esta constitución prevalece sobre cualquier otra práctica o instrucción del proyecto,
  incluido `CLAUDE.md`.
- Enmiendas: se proponen por Pull Request que modifique este archivo, explicando el motivo, y
  requieren aprobación del grupo.
- Versionado semántico: MAJOR si se elimina o redefine un principio; MINOR si se agrega un
  principio o sección; PATCH para aclaraciones de redacción.
- `/speckit-plan` verifica el cumplimiento de estos principios en su "Constitution Check"; toda
  excepción se justifica por escrito en el plan.

**Version**: 1.1.0 | **Ratified**: 2026-11-24 | **Last Amended**: 2026-11-24
