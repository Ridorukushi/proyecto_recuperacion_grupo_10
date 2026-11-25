---
name: crear-pantalla-angular
description: Procedimiento para crear una pantalla o componente del frontend Angular de Turismo Huila - componente standalone con signals, servicio HTTP, ruta, estados de carga/vacío/error y accesibilidad. Úsala al tocar frontend/src/.
---

# Crear una pantalla en Angular

1. **Modelo.** Define en `frontend/src/app/models/` las interfaces TypeScript que reflejan exactamente
   la respuesta del contrato de la API del `plan.md`.
2. **Servicio.** Las llamadas HTTP van en `frontend/src/app/services/<recurso>.service.ts`, con `inject(HttpClient)`
   y la URL base tomada de la configuración de entorno (nunca escrita a mano en el componente).
3. **Componente.** Standalone, con `ChangeDetectionStrategy.OnPush`. Estado con `signal()` y valores derivados con
   `computed()`. Plantilla con el control de flujo `@if`, `@for` (con `track`) y `@empty`.
4. **Tres estados obligatorios:** cargando, vacío con mensaje útil y error con opción de reintentar.
5. **Ruta.** Registra la pantalla en `app.routes.ts` con carga diferida (`loadComponent`). Los filtros que el usuario
   pueda querer compartir van en los parámetros de la URL.
6. **Presentación.** Precios con el formato de la skill `datos-turisticos`. Diseño móvil primero; `alt` en imágenes,
   `label` en campos, foco visible y orden de tabulación lógico.
7. **Prueba.** Ejecuta las pruebas del `probador` hasta que pasen sin modificarlas.
