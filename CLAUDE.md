@AGENTS.md

# Instrucciones propias de Claude Code

- Para tareas grandes, usa primero el modo plan y espera la aprobación del grupo antes de editar.
- Explica los cambios en palabras simples y en español: el grupo está aprendiendo.
- Al terminar una sesión de trabajo, usa el subagente `registrador-prompts` para dejar los prompts en `docs/prompts/`.
- Las skills de Spec Kit se invocan como `/speckit-specify`, `/speckit-plan`, etc. El comando `/nueva-spec` las encadena con los subagentes.
