---
paths:
  - "frontend/src/**"
---

# Reglas del frontend (Angular)

- Componentes standalone, estado con signals y `inject()` para dependencias. Sin NgModules.
- Toda llamada HTTP pasa por un servicio en `frontend/src/app/services/`; los componentes no usan `HttpClient` directamente.
- Cada pantalla que carga datos muestra sus estados: cargando, vacío y error con un mensaje claro y la opción de
  reintentar. Los textos exactos los fija la spec (en la 001: «No hay sitios para mostrar», «No hay sitios que
  coincidan con tu búsqueda» y «Sitio no encontrado»).
- Precios con el formato de la skill `datos-turisticos`; sin precio se muestra «Precio no disponible», nunca «$0».
- Enlaces externos (fuentes, mapa) con `target="_blank"` y `rel="noopener noreferrer"`.
- Diseño móvil primero. Imágenes con `alt`, controles navegables con teclado y etiquetas en los campos de formulario.
- Textos de la interfaz en español. Nada de llaves de API en el frontend.
