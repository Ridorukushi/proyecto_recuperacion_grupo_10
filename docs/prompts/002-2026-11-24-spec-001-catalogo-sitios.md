# Sesión 002 — Spec 001 catálogo de sitios (2026-11-24)

**Herramienta:** Claude Code (extensión de VS Code) · **Rama de trabajo:** `feat/001-catalogo-sitios` (sale de `recuperacion/olaya`)

Esta sesión construyó la spec 001 con el comando `/nueva-spec`, que encadena las skills `speckit-*` con los subagentes del arnés. Cada fase se detuvo a esperar la confirmación del grupo antes de avanzar.

### Prompt 1
**Prompt (textual):**
> `/nueva-spec 001-catalogo-sitios`

> Vamos a construir la spec **001-catalogo-sitios** con Spec Kit y el sistema de agentes del proyecto.
> Explica cada paso en palabras simples y **no avances al siguiente sin mi confirmación**.
> Tú eres el orquestador: coordinas y no programas. Las pruebas las escribe el `probador` y el código el `implementador`.
>
> 1. **Preparar.** Comprueba que `git status --short` esté vacío y que estemos en `recuperacion/olaya` actualizada.
>    Crea la rama `feat/001-catalogo-sitios` desde ahí.
> 2. **Prompt.** Ayúdame a redactar el pedido con la fórmula: *qué quiero, para quién, contexto, formato y restricciones*.
>    Guárdalo en `specs/001-catalogo-sitios/prompt.md` (plantilla en `docs/plantillas/prompt.md`).
> 3. **Spec.** Ejecuta `/speckit-specify` con ese prompt. Revisa que los criterios de aceptación se puedan probar.
>    Luego `/speckit-clarify` para resolver ambigüedades. **Espera mi aprobación de la spec.**
> 4. **Explorar.** Pide al subagente `explorador` lo reutilizable para esta spec.
> 5. **Plan.** Ejecuta `/speckit-plan` con el informe del explorador. El plan debe incluir el contrato de la API,
>    el modelo de datos y la tabla *criterio → prueba*. **Espera mi aprobación; sin ella no se escribe código.**
> 6. **Tareas.** Ejecuta `/speckit-tasks` (fases: Red, Green, Verificación, Cierre) y luego `/speckit-analyze`.
>    Resuelve los hallazgos críticos antes de seguir.
> 7. **Red.** Delega en `probador` las pruebas. Verifica su evidencia (fallan por el motivo esperado).
>    Commit de pruebas solo, antes del código.
> 8. **Green.** Delega en `implementador` las tareas de código. Si la verificación falla, máximo 2 vueltas; después
>    te detienes y me preguntas.
> 9. **Revisar.** `revisor-pull-request` siempre; `revisor-seguridad` si hay endpoints, base de datos, variables de
>    entorno o IA. Anota cada hallazgo en `specs/001-catalogo-sitios/revision.md` como aceptado (con commit) o descartado (con razón).
> 10. **Cerrar.** Crea `skills.md` con las skills, reglas y agentes usados. Marca `[X]` solo las tareas con evidencia.
>     Usa `registrador-prompts` para actualizar `docs/prompts/`. Muestra `git status --short -uall`, propón los
>     `git add` por ruta, los commits y el push. Abre el PR hacia `recuperacion/olaya` con la plantilla. **No fusiones.**

**Qué hizo Claude:** ejecutó `/nueva-spec` con el nombre `001-catalogo-sitios`. El comando sigue el orden del flujo: prompt → spec → clarify → plan → tasks → analyze → pruebas (Red) → código (Green) → revisores → Pull Request. Se usaron las skills `speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks` y `speckit-analyze`, y los subagentes `explorador`, `curador-datos`, `probador`, `implementador`, `revisor-pull-request` y `revisor-seguridad`.
**Resultado / commit:** se creó la rama `feat/001-catalogo-sitios` desde `recuperacion/olaya` y se inició la fase de preparación.

### Prompt 2
**Prompt (textual):**
> listo ya puse la spec 1 que sigue

**Qué hizo Claude:** confirmó que la carpeta de la spec 1 estaba lista y comenzó la revisión del estado del repositorio antes de avanzar.
**Resultado / commit:** sin commit; inicio de la sesión de trabajo.

### Prompt 3
**Prompt (textual):**
> Lee AGENTS.md, docs/ARNES.md, .specify/memory/constitution.md y docs/prompts/001-2026-11-24-configuracion-inicial.md para entender cómo quedó configurado el proyecto en la sesión anterior. Luego confirma que estamos en la rama recuperacion/olaya y dime en qué estado está el proyecto.

**Qué hizo Claude:** leyó la memoria del proyecto (`AGENTS.md`), el mapa del arnés (`docs/ARNES.md`), la constitución y el registro de la sesión 001. Revisó la rama y resumió el estado: arnés y constitución listos, spec 001 pendiente.
**Resultado / commit:** diagnóstico del estado del proyecto antes de empezar la spec.

### Prompt 4
**Prompt (textual):**
> nose la que usted considere la mas apropiada

**Qué hizo Claude:** el grupo delegó la decisión en Claude. Se tomó la propuesta más adecuada para la siguiente spec y se pidió confirmación antes de seguir.
**Resultado / commit:** se eligió el nombre de la spec `001-catalogo-sitios`.

### Prompt 5
**Prompt (textual):**
> guardelo asi

**Qué hizo Claude:** guardó la decisión tomada con el nombre propuesto y creó la carpeta `specs/001-catalogo-sitios/` con el archivo `prompt.md`.
**Resultado / commit:** prompt de la spec guardado.

### Prompt 6
**Prompt (textual):**
> si
> b
> si si si si si si
> ok
> ´si

**Qué hizo Claude:** estas son las confirmaciones que el grupo dio, en orden, para avanzar por las fases de **spec, clarify, plan, tasks, analyze, preparación, Red, Green y revisión**. Cada respuesta corta autorizó la siguiente fase. La opción «b» se usó en una pregunta de decisión de clarify o plan.

Fases y resultados:

- **Spec y clarify:** `/speckit-specify` y `/speckit-clarify`, con 3 aclaraciones (7 categorías de sitios, slug legible, precio mostrado como «Desde»).
  **Resultado / commit:** `bc130c7 docs: spec 001-catalogo-sitios aprobada (prompt, spec y checklist)`.
- **Explorar:** subagente `explorador` encontró 22 huecos. El grupo decidió usar PostgreSQL en el CI y que el orquestador prepare el esqueleto del proyecto.
- **Plan:** `/speckit-plan`, con research, modelo de datos, contrato OpenAPI, quickstart y la tabla de criterio → prueba.
  **Resultado / commit:** `2bb1230 docs: plan aprobado de la spec 001 (contrato OpenAPI, modelo de datos y criterio → prueba)`.
- **Tareas y analyze:** `/speckit-tasks` generó 51 tareas. `/speckit-analyze` encontró 9 hallazgos y se corrigieron 7.
  **Resultado / commit:** `7ae0973 docs: tareas de la spec 001 y ajustes de /speckit-analyze (I1, C1-C4, F1, U1)`.
- **Preparación:** el orquestador preparó el entorno: venv con `uv`, Angular 21, proxy de desarrollo, PostgreSQL en el CI y comandos oficiales en `AGENTS.md`. Se ajustaron la skill y la regla correspondientes.
  **Resultado / commit:** `4527c45 chore: preparar backend, frontend Angular 21, PostgreSQL en el CI y comandos oficiales`.
- **Datos (curador-datos):** 37 municipios y 10 sitios con fuentes. Decisión D-1: los precios de 2024 se mantienen, marcados como aproximados.
  **Resultado / commit:** `a35851d feat: catálogo inicial con 37 municipios y 10 sitios del Huila con fuentes`.
- **Red (probador):** 91 pruebas de backend y 35 de frontend que fallan por falta de código, con el criterio CA-1 a CA-20.
  **Resultado / commits:** `1776bc4 test: pruebas Red de la spec 001 (CA-1 a CA-20), sin código` y `30e6085 docs: evidencia del Red y decisiones del grupo en revision.md (spec 001)`.
- **Green (implementador):** código mínimo que hace pasar las pruebas. Hubo un bloqueo de entorno: faltaba el archivo de configuración local del backend y la clave de la base de datos no coincidía. Se resolvió creando un usuario de base de datos dedicado al proyecto.
  **Resultado / commits:** `edac5e3 feat: catálogo de sitios del Huila (API FastAPI, carga validada, lista y ficha en Angular)`, `bbcdf4a docs: evidencia del Green en revision.md (spec 001)` y `263ec20 test: ordenar imports de conftest (ruff I001)`.
- **Revisión:** `revisor-pull-request` encontró 14 hallazgos y `revisor-seguridad` encontró 7. Se aceptaron 17 y se descartaron 4, cada uno con su razón en `revision.md`.
  **Resultado / commits:** `2e7ec1e test: pruebas Red de los hallazgos de revisión (R1-R4, R6-R8, R12, S1, S2, S4, S7)`, `1b9481a docs: decisiones sobre los hallazgos de revisión y ajustes del modelo (spec 001)`, `558308b fix: correcciones de la revisión (recarga atómica, validación de filtros, errores en español, accesibilidad)` y `b9e21f9 docs: hashes de las correcciones en revision.md (spec 001)`.

### Prompt 7
**Prompt (textual):**
> ya terminó el explorador?
> ya terminó el implementador?
> ya terminó el revisor?
> ya terminó el probador?

**Qué hizo Claude:** respondió por cada subagente si había terminado, con su resultado y lo que seguía en el flujo. Las preguntas se hicieron mientras cada subagente trabajaba en segundo plano.
**Resultado / commit:** sin commit; seguimiento del avance.

### Prompt 8
**Prompt (textual):**
> los ejecuto yo?
> no se cual es la clave
> verifique
> cualquiera el que sea mejor
> listo

Se enviaron también capturas de pantalla de la terminal durante la configuración de PostgreSQL.

**Qué hizo Claude:** guio la configuración local de PostgreSQL paso a paso. Indicó qué comandos debía ejecutar el grupo y cuáles podía ejecutar Claude, verificó la conexión con la base de datos y recomendó un usuario dedicado al proyecto. Por seguridad, las claves no se registran en este archivo ni en el repositorio.
**Resultado / commit:** base de datos local lista para las pruebas del backend. Ningún secreto quedó en el repositorio.

### Prompt 9
**Prompt (textual):**
> pase directo al cierre

**Qué hizo Claude:** omitió las fases restantes y pasó al cierre de la spec: actualización de `skills.md`, marcado de tareas en `tasks.md` solo con evidencia, este registro de prompts y la preparación del Pull Request.
**Resultado / commit:** cierre de la spec 001. El Pull Request usa `.github/pull_request_template.md`. La tarea T044 (prueba manual de la interfaz) queda pospuesta por decisión del grupo.

---

**Notas de proceso**
- Los scripts de PowerShell de Spec Kit fueron bloqueados por el clasificador de permisos. El orquestador hizo esos pasos a mano, siguiendo las mismas plantillas.
- El hook `proteger-secretos` bloqueó una búsqueda que mencionaba el archivo de variables de entorno. No se leyó ni se editó ningún `.env`.
