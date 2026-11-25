# 001-catalogo-sitios: prompt

Pedido con el que el grupo arrancó la spec (2026-11-24), con la fórmula del curso:

- **Qué quiero:** un catálogo web de sitios turísticos del Huila con dos vistas:
  - una **lista** de sitios que se puede filtrar por municipio y por categoría, y buscar por nombre;
  - una **ficha** de cada sitio con nombre, descripción, municipio, categoría, precio aproximado en COP,
    horario, cómo llegar, fuente del dato y un enlace «Ver en mapa» (OpenStreetMap) con sus coordenadas.

  El catálogo inicial trae entre 10 y 15 sitios reales del Huila. Las categorías son: arqueología,
  naturaleza, aventura, cultura, religioso, gastronomía y termales (las 2 últimas se agregaron en
  `/speckit-clarify` para alinearse con la skill `datos-turisticos`).
- **Para quién:** turistas, colombianos o extranjeros, que planean visitar el Huila y quieren comparar
  sitios, costos y cómo llegar, sobre todo desde el celular.
- **Contexto:** es la primera spec del proyecto. Ya existe el arnés: constitución v1.1.0, `AGENTS.md`,
  reglas, skills, subagentes, hooks y CI. Todavía no hay código de la aplicación (no existen `backend/`
  ni `frontend/`), así que el `explorador` no encontrará nada reutilizable salvo las skills y reglas.
  Más adelante el asistente con IA usará este catálogo como su única fuente de datos.
- **Formato:** una spec con criterios de aceptación numerados (CA-1, CA-2…), cada uno comprobable con una
  prueba. Lo esperado al implementar:
  - backend: un endpoint para listar sitios (con filtros y búsqueda) y otro para ver un sitio;
  - datos: esquema en PostgreSQL y fichas iniciales armadas por el `curador-datos` en `backend/datos/`;
  - frontend: una pantalla de lista y una de detalle, con estados de carga, vacío y error.
- **Restricciones:**
  - pruebas primero (Red con el `probador`, Green con el `implementador`);
  - todo en español;
  - **sin datos inventados:** un dato desconocido se deja vacío; sin precio se muestra «Precio no disponible»;
  - precio con el formato `$25.000 COP (aprox., consultado en nov. 2026)`;
  - coordenadas dentro del Huila (latitud 1.5 a 3.9, longitud −76.6 a −74.4), validadas en el backend;
  - cada ficha con su fuente;
  - responsive (móvil primero) y accesibilidad básica;
  - sin mapa embebido ni dependencias de mapas: solo el enlace a OpenStreetMap;
  - **fuera de alcance:** el asistente con IA, cuentas de usuario y edición del catálogo desde la web.

**Skills que debe usar:** `datos-turisticos`, `escribir-pruebas`, `crear-endpoint-fastapi`,
`crear-pantalla-angular` y las `speckit-*`.

**Aprobaciones:** prompt aprobado por el grupo el 2026-11-24. Spec aprobada por el grupo el 2026-11-24
(después de `/speckit-clarify`). Plan: pendiente.
