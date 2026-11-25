---
description: "Guía una spec completa: prompt, Spec Kit (specify, clarify, plan, tasks, analyze), pruebas primero con el probador, código con el implementador, revisores, evidencia y Pull Request."
argument-hint: "<NNN-nombre> (por ejemplo 001-catalogo-sitios)"
---

Vamos a construir la spec **$ARGUMENTS** con Spec Kit y el sistema de agentes del proyecto.
Explica cada paso en palabras simples y **no avances al siguiente sin mi confirmación**.
Tú eres el orquestador: coordinas y no programas. Las pruebas las escribe el `probador` y el código el `implementador`.

1. **Preparar.** Comprueba que `git status --short` esté vacío y que estemos en `recuperacion/olaya` actualizada.
   Crea la rama `feat/$ARGUMENTS` desde ahí.
2. **Prompt.** Ayúdame a redactar el pedido con la fórmula: *qué quiero, para quién, contexto, formato y restricciones*.
   Guárdalo en `specs/$ARGUMENTS/prompt.md` (plantilla en `docs/plantillas/prompt.md`).
3. **Spec.** Ejecuta `/speckit-specify` con ese prompt. Revisa que los criterios de aceptación se puedan probar.
   Luego `/speckit-clarify` para resolver ambigüedades. **Espera mi aprobación de la spec.**
4. **Explorar.** Pide al subagente `explorador` lo reutilizable para esta spec.
5. **Plan.** Ejecuta `/speckit-plan` con el informe del explorador. El plan debe incluir el contrato de la API,
   el modelo de datos y la tabla *criterio → prueba*. **Espera mi aprobación; sin ella no se escribe código.**
6. **Tareas.** Ejecuta `/speckit-tasks` (fases: Red, Green, Verificación, Cierre) y luego `/speckit-analyze`.
   Resuelve los hallazgos críticos antes de seguir.
7. **Red.** Delega en `probador` las pruebas. Verifica su evidencia (fallan por el motivo esperado).
   Commit de pruebas solo, antes del código.
8. **Green.** Delega en `implementador` las tareas de código. Si la verificación falla, máximo 2 vueltas; después
   te detienes y me preguntas.
9. **Revisar.** `revisor-pull-request` siempre; `revisor-seguridad` si hay endpoints, base de datos, variables de
   entorno o IA. Anota cada hallazgo en `specs/$ARGUMENTS/revision.md` como aceptado (con commit) o descartado (con razón).
10. **Cerrar.** Crea `skills.md` con las skills, reglas y agentes usados. Marca `[X]` solo las tareas con evidencia.
    Usa `registrador-prompts` para actualizar `docs/prompts/`. Muestra `git status --short -uall`, propón los
    `git add` por ruta, los commits y el push. Abre el PR hacia `recuperacion/olaya` con la plantilla. **No fusiones.**
