# Sesión 001 — Configuración inicial (2026-11-24)

**Herramienta:** Claude Code (extensión de VS Code) · **Rama:** `recuperacion/olaya`

### Prompt 1
**Prompt (textual):**
> analice todos los archivos de mi proyecto ya le digo que toca hacer

**Qué hizo Claude:** listó y leyó los archivos del proyecto local. Encontró solo una plantilla
vacía de Angular 21 sin código propio.
**Resultado:** diagnóstico del estado inicial.

### Prompt 2
**Prompt (textual):**
> tengo que realizar un proyecto acerca de sitios turisticos del huila, en el se van a encontrar
> los precios aproximados , ubicaciones, etc... [...] Se nos exige tener un plan, usar skill,
> agentes, speckit con sus specs, los promps [...] necesito que me esplique como puedo empezar a
> desarrollar eso por medio unicamente de cloud code.

**Qué hizo Claude:** explicó el flujo completo: Spec Kit (constitución → specify → clarify → plan
→ tasks → analyze → implement), skills en `.claude/skills`, subagentes en `.claude/agents`,
`CLAUDE.md`, registro de prompts y flujo de Git/GitHub con ramas y Pull Requests.
**Resultado:** hoja de ruta por fases (0: preparación, 1: SDD, 2: skills y agentes, 3: ciclo diario).

### Prompt 3
**Prompt (textual):**
> mejor creenme un repositorio que se llame asi: proyecto_recuperacion_grupo_10, y pongale el
> nombre de la rama que ya le habia dicho

**Qué hizo Claude:** instaló GitHub CLI (`winget install GitHub.cli`). El usuario inició sesión
con `gh auth login`.

### Prompt 4
**Prompt (textual):**
> el repositorio va hacer publico y no vayas a copiar nada de otro lado

**Qué hizo Claude:** creó el repo público `Ridorukushi/proyecto_recuperacion_grupo_10` desde cero,
con un README inicial en `main`. Creó y subió la rama `recuperacion/olaya`.
**Resultado / commit:** `67abb42 chore: commit inicial con README`

### Prompt 5
**Prompt (textual):**
> listo ahora si sigamos

**Qué hizo Claude:** instaló Spec Kit con integración para Claude:
`uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude --script ps`.
Creó `CLAUDE.md` (memoria del proyecto), `.gitattributes` y este registro de prompts.
**Resultado / commits:** `1df086e chore: instalar Spec Kit con integración para Claude Code` y
`18e52dd docs: agregar CLAUDE.md, registro de prompts y .gitattributes`.

### Prompt 6
**Prompt (textual):**
> con frontend y con backend. recuerde que debemos tener agentes, debemos tener los archivos promps, el plan, etc...

**Qué hizo Claude:**
- Ejecutó el flujo de la skill `speckit-constitution`: resolvió la plantilla con
  `resolve-template.ps1` y redactó la constitución v1.0.0 con 5 principios. El stack quedó en
  Angular, FastAPI, PostgreSQL y la API de Claude.
- Creó 4 subagentes en `.claude/agents/`: `curador-datos`, `revisor-codigo`, `tester` y
  `registrador-prompts`.
- Creó la skill propia `datos-turisticos` en `.claude/skills/`.
- Actualizó `CLAUDE.md`.

**Resultado / commits:** `294ca40 docs: ratificar constitución v1.0.0` y
`317e2c4 feat: agregar subagentes del proyecto y skill datos-turisticos`.

### Prompt 7
**Prompt (textual):**
> si, aqui te dejo de un repositorio que les quedo bien el proyecto para que se guie de la estructura de las
> cosas que ellos tenian https://github.com/juandadevp/cuentasclaras.git

**Qué hizo Claude:**
- Clonó el repositorio de referencia en una carpeta temporal fuera del proyecto y estudió **solo su
  estructura**. No copió código ni textos: todo se redactó de nuevo para Angular, FastAPI y PostgreSQL.
- Estructura que adoptó:
  - memoria en `AGENTS.md`, importada desde `CLAUDE.md`;
  - reglas por ruta en `.claude/rules/`;
  - subagentes con roles Red/Green (`explorador`, `probador`, `implementador`, `revisor-pull-request`
    y `revisor-seguridad`), que reemplazan a `tester` y `revisor-codigo`;
  - hooks que hacen cumplir los permisos (`limitar-agente.mjs` y `proteger-secretos.mjs`, con 7 pruebas);
  - `.claude/settings.json`;
  - el comando `/nueva-spec`;
  - las skills `escribir-pruebas`, `crear-endpoint-fastapi` y `crear-pantalla-angular`;
  - evidencia por spec (`prompt.md`, `skills.md`, `revision.md`, con plantillas en `docs/plantillas/`);
  - `docs/ARNES.md`, la plantilla de PR y el CI de GitHub Actions.
- Diferencia con la referencia: aquí sí se usa Spec Kit, así que `/nueva-spec` encadena las skills
  `speckit-*` con los subagentes.
- Enmendó la constitución a v1.1.0 (MINOR): agregó la estrategia de ramas `feat/NNN-*` hacia
  `recuperacion/olaya`, la separación Red/Green y la evidencia por spec.

**Resultado / commits:** cinco commits, en este orden:
- `a4df445 docs: enmendar constitución a v1.1.0 (ramas feat/NNN, Red/Green y evidencia por spec)`
- `3bce8ad docs: memoria del proyecto en AGENTS.md y reglas por ruta en .claude/rules`
- `80dcdae feat: subagentes Red/Green con permisos reforzados por hooks`
- `6e0bc78 feat: comando /nueva-spec y skills escribir-pruebas, crear-endpoint-fastapi y crear-pantalla-angular`
- `46cb66f docs: mapa del arnés, plantillas de evidencia, plantilla de PR y CI`
