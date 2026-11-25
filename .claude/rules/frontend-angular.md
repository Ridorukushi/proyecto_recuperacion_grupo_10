---
paths:
  - "frontend/src/**"
---

# Reglas del frontend (Angular)

- Componentes standalone, estado con signals y `inject()` para dependencias. Sin NgModules.
- Toda llamada HTTP pasa por un servicio en `frontend/src/app/services/`; los componentes no usan `HttpClient` directamente.
- Cada pantalla que carga datos muestra tres estados: cargando, vacío («No hay sitios con esos filtros») y error con un mensaje claro.
- Precios con el formato de la skill `datos-turisticos`; sin precio se muestra «Precio no disponible», nunca «$0».
- Diseño móvil primero. Imágenes con `alt`, controles navegables con teclado y etiquetas en los campos de formulario.
- Textos de la interfaz en español. Nada de llaves de API en el frontend.
