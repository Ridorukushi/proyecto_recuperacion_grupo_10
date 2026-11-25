## Spec
<!-- Número y nombre, por ejemplo: 001-catalogo-sitios -->

## Qué incluye
<!-- 3 a 5 viñetas de lo que hace -->
-

## Evidencia del proceso
- Carpeta: `specs/NNN-nombre/` (`prompt.md`, `spec.md`, `plan.md`, `tasks.md`, `skills.md`, `revision.md`)
- Prompts de la sesión: `docs/prompts/…`
- Skills usadas: <!-- de .claude/skills/ -->

## Cómo se probó
- [ ] Pruebas del backend (pytest)
- [ ] Pruebas del frontend (vitest) y build de Angular
- [ ] `node --test .claude/hooks/hooks.test.mjs`
- [ ] Probado en pantalla (captura o descripción)

## Evidencia de calidad
- [ ] Las pruebas se subieron en un commit anterior al del código: <!-- enlace a cada commit -->
- [ ] El `probador` confirmó el Red (cada prueba falló por el motivo esperado)
- [ ] Informe de `revisor-pull-request` y, si aplica, de `revisor-seguridad`
- [ ] Cada hallazgo tiene su decisión en `revision.md`

## Revisión del arnés y de los datos
- [ ] La spec y el plan se aprobaron antes de escribir código
- [ ] Sin claves ni `.env` en los cambios; variables nuevas en `.env.example`
- [ ] Precios en COP aproximados con fecha y fuente; ningún dato inventado
- [ ] Ningún archivo importado quedó sin subir
