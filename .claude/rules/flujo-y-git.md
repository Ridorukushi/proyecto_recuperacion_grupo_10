# Flujo de trabajo y git (se aplica siempre)

- Cada spec tiene su carpeta `specs/NNN-nombre/` y su rama `feat/NNN-nombre`, que sale de `recuperacion/olaya`.
- Orden: prompt → spec → clarify → plan → tasks → analyze → pruebas (Red) → código (Green) → revisores → Pull Request.
- Una persona del grupo aprueba la spec y el plan antes de que se escriba código. Ningún agente fusiona ramas.
- Las pruebas se suben en su propio commit, antes del commit del código que las hace pasar.
- Commits cortos, en español, con prefijo convencional. Los archivos se agregan por su ruta: nunca `git add .` ni `git add -A`.
- Prohibido: `git push --force`, `git reset --hard` y cualquier lectura o edición de `.env` (salvo `.env.example`).
- El Pull Request usa `.github/pull_request_template.md` y no se fusiona hasta que el CI esté en verde.
- Cada hallazgo de un revisor se anota en `revision.md`: aceptado (con el commit que lo arregla) o descartado (con la razón).
- Una tarea se marca `[X]` en `tasks.md` solo si hay evidencia (prueba en verde o commit).
