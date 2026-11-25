# Frontend de Turismo Huila

Aplicación Angular (componentes standalone y signals) con la lista y la ficha de los sitios turísticos del Huila.
Consume la API del backend; nunca llama directamente a la IA.

## Comandos

Desde esta carpeta (`frontend/`):

- `npm install`: instala las dependencias.
- `npx ng serve`: servidor de desarrollo en http://localhost:4200, con proxy a la API en `localhost:8000`.
- `npx ng test --watch=false`: ejecuta las pruebas (vitest).
- `npm run build`: genera la versión de producción en `dist/`.

## Más información

Especificación, plan y tareas: [specs/001-catalogo-sitios](../specs/001-catalogo-sitios).
